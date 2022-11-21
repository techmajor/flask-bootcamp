from flask import Flask, request
from db import products
import uuid

app = Flask(__name__)

@app.get("/")
def get_hello():
  return "hello world"

@app.get("/products")
def get_products():
  return products

@app.post("/products")
def create_product():
  # Get request data
  request_data = request.get_json()
  # create new product
  product_id = uuid.uuid4().hex
  new_product = {product_id: {"name": request_data["name"], "price": request_data["price"]}}
  products.update(new_product)
  # products[product_id] = {"name": request_data["name"], "price": request_data["price"]}
  return new_product, 201

##############
# Dynamic urls
##############
@app.post("/products/<string:product_id>/rate")
def add_rating(product_id):
  # Get request data
  request_data = request.get_json()
  try:
    if "ratings" not in products[product_id]:
      products[product_id]["ratings"] = []
      
    new_rating = request_data["rating"]
    products[product_id]["ratings"].append(new_rating)
    return products[product_id]["ratings"], 201
  except KeyError:
    return {"message": "Product not found"}, 404

@app.get("/products/<string:product_id>")
def get_product(product_id):
  try:
    return products[product_id], 200
  except KeyError:
    return {"message": "Product not found"}, 404

@app.get("/products/<string:product_id>/ratings")
def get_product_ratings(product_id):
  try:
    if "ratings" not in products[product_id]:
      return {"message": "No ratings for product"}, 200
    return products[product_id]["ratings"], 200
  except KeyError:
    return {"message": "Product not found"}, 404
