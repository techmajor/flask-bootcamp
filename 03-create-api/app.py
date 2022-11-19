from flask import Flask, request

app = Flask(__name__)

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
  
