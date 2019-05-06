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
def add_product():
    try:
        handle_name = request.json["handle"]
        product = Product.query.filter_by(handle=handle_name).first()
        if product:
            raise NameError

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

    return "Created.", 201


@app.route("/storage/<product>/add/", methods=["POST"])
def add_to_storage(product):
    try:
        product = Product.query.filter_by(handle=product).first()
        if product:
            qty=int(request.json["qty"])
            location=str(request.json["location"])
            stor = StorageItem(
                qty=qty,
                product_id=product.id,
                location=location
            )
            db.session.add(stor)
            db.session.commit()
        else:
            raise TypeError
            
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

    return "Created.", 201


@app.route("/storage/", methods=["GET"])
def get_inventory():

    if request.method == "GET":
        response_data = []
        products = Product.query.all()

        for product in products:
            inventory = []
            for inv in product.products:
                inventory.append([inv.location, inv.qty])

            response_data.append({
                "handle": product.handle,
                "weight": product.weight,
                "price": product.price,
                "inventory": inventory,
            })

    return json.dumps(response_data)
