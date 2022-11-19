from flask import Flask

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

