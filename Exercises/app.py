from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    
@app.route("/products/add", methods=["POST"])
def add_product(product_name):
    # This branch happens when user submits the form
    try:
        product = Product.query.filter_by(name=product_name).first()
        if product:
            handle = str(request.json["handle"])
            weight = float(request.json["weight"])
            price = float(request.json["price"])
            prod = Product(
                id=id,
                handle=handle,
                weight=weight,
                price=price,
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
    
    
@app.route("/storage/<product>/add")
def add_to_storage(storage_name):
    # This branch happens when user submits the form
    try:
        storage = Storage.query.filter_by(name=storage_name).first()
        if storage:
            id=id
            qty=int(request.json["qty"])
            product_id=product_id
            location=str(request.json["location"])
            stor = Storage(
                id=id
                qty=qty
                product_id=product_id
                location=location
            )
            db.session.add(stor)
            db.session.commit()
            
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
    return 201
        
@app.route("/storage/", methods=["GET"])
    def get_inventory(req):
        
















