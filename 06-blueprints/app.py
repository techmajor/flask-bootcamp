from flask import Flask, request, Blueprint
from db import products
import uuid
from products.routes import product_bp
from reviews.routes import reviews_bp

app = Flask(__name__)

app.register_blueprint(product_bp)
app.register_blueprint(reviews_bp)

@app.get("/")
def get_hello():
  return "hello world"
