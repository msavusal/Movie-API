from flask import Flask, request, json, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from sqlalchemy.engine import Engine
from sqlalchemy import event

from flask_restful import Resource, Api
from jsonschema import validate, ValidationError

"""
CONFIGURATION AND VARIABLES
"""
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__, static_folder="static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

api = Api(app)

MASON = "application/vnd.mason+json"
LINK_RELATIONS_URL = "/storage/link-relations/"
PRODUCT_PROFILE = "/profiles/product/"
STORAGE_PROFILE = "/profiles/storage/"
ERROR_PROFILE = "/profiles/error/"


"""
MASON BUILDER
"""
class MasonBuilder(dict):
    def add_namespace(self, ns, uri):
        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

    def add_error(self, title, details):
       self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

# Error response helper function
def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)


"""
DB MODELS
"""
class StorageEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    location = db.Column(db.String(64), nullable=False)

    product = db.relationship("Product", back_populates="in_storage")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    in_storage = db.relationship("StorageEntry", back_populates="product")

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["handle", "weight", "price"]
        }
        props = schema["properties"] = {}
        props["handle"] = {
            "description": "Product's unique name",
            "type": "string"
        }
        props["weight"] = {
            "description": "Product's weight",
            "type": "number"
        }
        props["price"] = {
            "description": "Product's price",
            "type": "number"
        }
        return schema


deployments = db.Table("deployments",
    db.Column("storage_entry_id",db.Integer, db.ForeignKey("storage_entry.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True)
)

# Create database models
db.create_all()


"""
RESOURCES
"""
class ProductItem(Resource):

    def get(self, handle):
        db_product = Product.query.filter_by(handle=handle).first()
        if db_product is None:
            return create_error_response(404, "Not found",
                "No product was found with the name {}".format(handle)
            )

        body = InventoryBuilder(
            handle=db_product.handle,
            weight=db_product.weight,
            price=db_product.price
        )

        body.add_namespace("storage", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(ProductItem, handle=handle))
        body.add_control("profile", STORAGE_PROFILE)
        body.add_control("collection", api.url_for(ProductCollection))
        body.add_control_edit_product(handle)
        body.add_control_delete_product(handle)

        return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, handle):
        if not request.json:
            return create_error_response(415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(request.json, Product.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_product = Product.query.filter_by(handle=handle).first()
        if db_product is None:
            return create_error_response(404, "Not found",
                "No product was found with the name {}".format(handle)
            )

        db_product.handle = request.json["handle"]
        db_product.weight = request.json["weight"]
        db_product.price = request.json["price"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists",
                "Product with handle '{}' already exists.".format(request.json["handle"])
            )

        return Response(status=204, mimetype=MASON)

    def delete(self, handle):
        db_product = Product.query.filter_by(handle=handle).first()
        if db_product is None:
            return create_error_response(404, "Not found",
                "No product was found with the name {}".format(handle)
            )

        db.session.delete(db_product)
        db.session.commit()

        return Response(status=204, mimetype=MASON)


class ProductCollection(Resource):

    def get(self):
        db_products = Product.query.all()

        if db_products is None:
            return create_error_response(404, "Not found",
                "There are no products in the database."
            )

        body = InventoryBuilder(items=[])

        for product in db_products:
            item = InventoryBuilder(
                handle=product.handle,
                weight=product.weight,
                price=product.price
            )

            item.add_control("self", api.url_for(ProductItem, handle=product.handle))
            item.add_control("profile", STORAGE_PROFILE)
            body["items"].append(item)

        body.add_namespace("storage", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(ProductCollection))
        body.add_control_add_product()

        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        if not request.json:
            return create_error_response(415, "Unsupported media type",
                "Requests must be JSON"
            )

        try:
            validate(request.json, Product.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        prod = Product(
            handle=request.json["handle"],
            weight=float(request.json["weight"]),
            price=float(request.json["price"])
        )

        try:
            db.session.add(prod)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists",
                "Product with handle '{}' already exists.".format(request.json["handle"])
            )

        return Response(status=201, headers={
            "Location": api.url_for(ProductItem, handle=request.json["handle"])
        }, mimetype=MASON)


"""
CUSTOM MASON BUILDERS
"""
class InventoryBuilder(MasonBuilder):

    def add_control_all_products(self):
        self.add_control(
            "storage:products-all",
            href=api.url_for(ProductCollection),
            method="GET",
            encoding="json",
            title="Get all products"
        )

    def add_control_delete_product(self, handle):
        self.add_control(
            "storage:delete",
            href=api.url_for(ProductItem, handle=handle),
            method="DELETE",
            title="Delete this product"
        )

    def add_control_add_product(self):
        self.add_control(
            "storage:add-product",
            href=api.url_for(ProductCollection),
            method="POST",
            encoding="json",
            title="Add a new product",
            schema=Product.get_schema()
        )

    def add_control_edit_product(self, handle):
        self.add_control(
            "edit",
            href=api.url_for(ProductItem, handle=handle),
            method="PUT",
            encoding="json",
            title="Edit this product",
            schema=Product.get_schema()
        )


"""
URL MAPPING
"""
@app.route('/api/')
def entry():
    body = InventoryBuilder()
    body.add_namespace("storage", "/storage/link-relations/#")
    body.add_control_all_products()

    return Response(json.dumps(body))

@app.route("/profiles/<resource>/")
def send_profile_html(resource):
    return Response("", 200, mimetype=MASON)

@app.route("/storage/link-relations/")
def send_link_relations_html():
    return Response("", 200, mimetype=MASON)

api.add_resource(ProductCollection, "/api/products/")
api.add_resource(ProductItem, "/api/products/<handle>")
