from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from db import db, products
import uuid
from schemas import ProductSchema, ProductRatingSchema, RatingsResponseSchema, ProductListSchema
from models.products import ProductModel
from sqlalchemy.exc import SQLAlchemyError
from ..utils import row2dict

product_bp = Blueprint("products_blueprint", __name__, description="products bp")

# Get individual product.
# Model.query.get_or_404(product_id)
@product_bp.route("/products/<string:product_id>")
class Product(MethodView):
  @product_bp.response(200, ProductSchema)
  def get(self, product_id):
    try:
      product = ProductModel.query.get_or_404(product_id, "Product not found")
      return product.getDict()
      # return row2dict(product)
    except SQLAlchemyError:
      return {"message": "Product not found"}, 404
  
  @product_bp.arguments(ProductSchema)
  def put(self,request_data, product_id):
    try:
      # request_data = request.get_json()
      product = ProductModel.query.get(product_id)
      if product:
        product = ProductModel.query.get(product_id)
        product.name = request_data["name"]
        product.price = request_data["price"]
      else:
        product = ProductModel(**request_data)
        product.id = product_id
      
      db.session.add(product)
      db.session.commit()
      return product.getDict(), 203
    except SQLAlchemyError:
      return {"message": "Unable to insert into DB."}
  
  def delete(self, product_id):
      product = ProductModel.query.get_or_404(product_id)
      db.session.delete(product)
      db.session.commit()
      return {"message": "Product deleted"}

# Get all products
# Two ways of doing it.
# 1. db.session.query(ProductModel)
# 2. ProductModel.query.all() 
# But the response cannot be directly converted to JSON.
# Convert the result to a list of dicts before returning.
@product_bp.route("/products")
class ProductList(MethodView):
  @product_bp.response(200, ProductSchema(many=True))
  # @product_bp.response(200, ProductListSchema(many=True))
  def get(self):
    try:
      # prods = db.session.query(ProductModel)
      prods = ProductModel.query.all()
      resp = []
      for prod in prods:
        resp.append(prod.getDict())
        # resp.append(row2dict(prod))
      return resp
    except SQLAlchemyError:
      return {"message": "Something went wrong"}, 500
    
  # Create product (insert new product to the table)
  # 1. Create a new object of type Model (ProductModel) and populate the necessary fields
  # 2. add object to session -- db.session.add()
  # 3. Commit session -- db.session.commit()
  # Convert to dict and return.
  @product_bp.arguments(ProductSchema)
  def post(self, request_data):
    # insert into db.
    try:
      # pm = ProductModel(name=request_data["name"], price=request_data["price"])
      pm = ProductModel(**request_data)
      db.session.add(pm)
      db.session.commit()
      print(pm.id)
      
      product_id = str(pm.id) #uuid.uuid4().hex
      new_product = {product_id: {"name": request_data["name"], "price": request_data["price"]}}
      products.update(new_product)
      return pm.getDict(), 201
    except SQLAlchemyError:
      return {"message": "Could not insert new Product into DB"}, 500
    
  
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