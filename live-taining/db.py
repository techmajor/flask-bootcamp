from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#defining te resource
products = {
  "1": {
    "name": "Iphone 14",
    "price": 100000,
    "abcd": "something"
  },
  "2": {
    "name": "iPhone 13",
    "price": 50000
  }
}

reviews = {
  "1": {
    "product_id": "1",
    "review_text": "Awesome product!!"
  }
}