from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from db import products
import uuid
from schemas import ProductSchema, ProductRatingSchema, RatingsResponseSchema

product_bp = Blueprint("products_blueprint", __name__, description="products bp")

@product_bp.route("/products/<string:product_id>")
class Product(MethodView):
  @product_bp.arguments(ProductSchema)
  def get(self, product_id):
    try:
      return products[product_id]
    except KeyError:
      return {"message": "Product not found"}, 404
    
@product_bp.route("/products")
class ProductList(MethodView):
  def get(self):
    return products
  
  @product_bp.arguments(ProductSchema)
  def post(self, request_data):
    # Get request data
    # request_data = request.get_json()
    # create new product
    product_id = uuid.uuid4().hex
    new_product = {product_id: {"name": request_data["name"], "price": request_data["price"]}}
    products.update(new_product)
    # products[product_id] = {"name": request_data["name"], "price": request_data["price"]}
    return new_product, 201
  
@product_bp.route("/products/<string:product_id>/ratings")
class ProductRating(MethodView):
  @product_bp.response(200, RatingsResponseSchema)
  def get(self, product_id):
    try:
      if "ratings" not in products[product_id]:
        return {"message": "No ratings for product"}, 200
      return { "ratings": products[product_id]["ratings"]}, 200
    except KeyError:
      return {"message": "Product not found"}, 404
  
  @product_bp.arguments(ProductRatingSchema)
  @product_bp.response(201, RatingsResponseSchema)
  def post(self, request_data, product_id):
    # Get request data
    # request_data = request.get_json()
    try:
      if "ratings" not in products[product_id]:
        products[product_id]["ratings"] = []
        
      new_rating = request_data["rating"]
      products[product_id]["ratings"].append(new_rating)
      return { "ratings": products[product_id]["ratings"]}, 201
    except KeyError:
      return {"message": "Product not found"}, 404