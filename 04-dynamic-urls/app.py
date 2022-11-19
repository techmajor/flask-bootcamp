from flask import Flask, request

app = Flask(__name__)
app.debug = True

products = [
  {
    "name": "abcd",
    "price": 10
  }
]

@app.get("/")
def get_hello():
  return "hello world"

@app.get("/products")
def get_products():
  return {"products": products}

@app.post("/products")
def create_product():
  # Get request data
  request_data = request.get_json()
  # create new product
  new_product = {"name": request_data["name"], "price": request_data["price"]}
  # Append it to the list of products
  products.append(new_product)
  
  return new_product, 201

##############
# Dynamic urls
##############
@app.post("/products/<string:name>/rate")
def add_rating(name):
  # Get request data
  request_data = request.get_json()
  for prod in products:
    # Find the product whose rating is to be added
    if prod["name"] == name:
      # Read rating from request data
      new_rating = request_data["rating"]
      # create 'ratings' list, if it doesn't exist
      if "ratings" not in prod:
        prod["ratings"] = []
      # Append new rating and return
      prod["ratings"].append(new_rating)
      return prod["ratings"], 201
    
  return {"message": "Product not found"}, 404

@app.get("/products/<string:name>")
def get_product(name):
  for prod in products:
    # Find the product
    if prod["name"] == name:
      return prod, 200
  return {"message": "Product not found"}, 404

@app.get("/products/<string:name>/ratings")
def get_product_ratings(name):
  for prod in products:
    # Find the product
    if prod["name"] == name:
      return prod["ratings"], 200
  return {"message": "Product not found"}, 404
