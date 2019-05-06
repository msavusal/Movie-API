from flask import Flask, request, json, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from sqlalchemy.engine import Engine
from sqlalchemy import event

from flask_restful import Resource, Api


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

api = Api(app)

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


class StorageEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    location = db.Column(db.String(64), nullable=False)

    product = db.relationship("Product", back_populates="products")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    products = db.relationship("StorageEntry", back_populates="product")


deployments = db.Table("deployments",
    db.Column("storage_entry_id",db.Integer, db.ForeignKey("storage_entry.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True)
)

db.create_all()


class ProductItem(Resource):

    def get(self, handle):
        return Response(status=501)


class ProductCollection(Resource):

    def get(self):
        products = Product.query.all()
        response_data = []

        for product in products:
            response_data.append({
                "handle": product.handle,
                "weight": product.weight,
                "price": product.price
            })

        return response_data

    def post(self):
        headers = {}
        try:
            handle_name = request.json["handle"]
            product = Product.query.filter_by(handle=handle_name).first()
            if product:
                raise NameError

            weight = float(request.json["weight"])
            price = float(request.json["price"])
            prod = Product(
                handle=handle_name,
                weight=weight,
                price=price
            )
            db.session.add(prod)
            db.session.commit()

        except NameError:
            return "Handle already exists", 409
        except KeyError:
            return "Incomplete request - missing fields", 400
        except TypeError:
            return "Request content type must be JSON", 415
        except ValueError:
            return "Weight and price must be numbers", 400
        except IntegrityError:
            return "POST method required", 405

        return Response(status=201, headers={
            "Location": api.url_for(ProductItem, handle=handle_name)
        })


class InventoryBuilder(MasonBuilder):
    @staticmethod
    def product_schema():
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
            schema=self.product_schema()
        )

    def add_control_edit_product(self, handle):
        self.add_control(
            "edit",
            href=api.url_for(ProductItem, handle=handle),
            method="PUT",
            encoding="json",
            title="Edit this product",
            schema=self.product_schema()
        )


api.add_resource(ProductCollection, "/api/products/")
api.add_resource(ProductItem, "/api/products/<handle>")

if __name__ == '__main__':
    app.run(debug=True)
