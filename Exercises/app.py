from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

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
    db.Column("storage_item_id", db.Integer, db.ForeignKey("storage_item.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True)
)

db.create_all()

@app.route("/products/add/", methods=["POST"])
def add_product(product_name):
    if request.method == "POST":
    # This branch happens when user submits the form
        try:
            product = Product.query.filter_by(handle=product_name).first()
            if product:
                handle = str(request.json["handle"])
                weight = float(request.json["weight"])
                price = float(request.json["price"])
                prod = Product(
                    handle=handle,
                    weight=weight,
                    price=price
                )
                db.session.add(prod)
                db.session.commit()
            else:
                abort(404)
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
    return 201


@app.route("/storage/<product>/add/", methods=["POST"])
def add_to_storage(product):
    if request.method == "POST":
    # This branch happens when user submits the form
        try:
            storage = StorageItem.query.filter_by(name=product).first()
            if storage:
                id=id
                qty=int(request.json["qty"])
                product_id=product_id
                location=str(request.json["location"])
                stor = Storage(
                    id=id,
                    qty=qty,
                    product_id=product_id,
                    location=location
                )
                db.session.add(stor)
                db.session.commit()
            else:
                abort(404)
        except NameError:
            return "Handle already exists", 409
        except KeyError:
            return "Incomplete request - missing fields", 400
        except TypeError:
            return "Product not found", 404
        except ValueError:
            return "Qty must be an integer", 400
        except IntegrityError:
            return "POST method required", 405
        except IntegrityError:
            return "Request content type must be JSON", 415
    return 201

@app.route("/storage/", methods=["GET"])
def get_inventory():
    if request.method == "GET":
        response_data = []
        storage = StorageItem.query.all()
        for product in storage:
            response_data.append([product.handle, product.weight, product.price, product.inventory])
    return json.dumps(response_data)
