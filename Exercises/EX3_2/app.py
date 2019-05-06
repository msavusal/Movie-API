from flask import Flask, request, json, Response, Blueprint
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

api = Api(app, url_part_order="eba")


class StorageItem(db.Model):
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

    products = db.relationship("StorageItem", back_populates="product")


deployments = db.Table("deployments",
    db.Column("storage_item_id",db.Integer, db.ForeignKey("storage_item.id"), primary_key=True),
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


api.add_resource(ProductCollection, "/api/products/", endpoint="api")
api.add_resource(ProductItem, "/api/products/<handle>/")

@app.route("/")
def index():
    return ""
