from flask_smorest import Blueprint
from flask.views import MethodView
from db import products, db
from flask import request
import uuid
from schema import ProductSchema, ProductRatingsSchema, RatingsResponseSchema
from models.Products import ProductModel
from models.utils import row2Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

products_bp = Blueprint("Products", __name__, description="Operations on products")

@products_bp.route("/products")
class ProductListView(MethodView):
  def get(self):
    try:
      products = ProductModel.query.all()
      # return [product.getDict() for product in products ]
      ret = []
      for product in products:
        ret.append(product.getDict())
      return ret, 200
    except SQLAlchemyError as e:
      print(str(e))
      return {"message": "no product"}
  
  @products_bp.arguments(ProductSchema)
  @products_bp.response(200, ProductSchema)
  def post(self, request_data):
    # 1. Create a ProductModel
    # product = ProductModel(name=request_data["name"], price=request_data["price"])
    
    # 2. Populate the fields appropriately
    product = ProductModel(**request_data)
    # 3. Add the object to session
    db.session.add(product)
    # 4. Commit.
    db.session.commit()
    
    print("id: " + str(product.id))
    
    return product.getDict(), 200

@products_bp.route("/products/<string:product_id>")
class ProductView(MethodView):
  def get(self, product_id):
    product = ProductModel.query.get_or_404(product_id)
    return product.getDict(), 200
  
  def delete(self, product_id):
    product = ProductModel.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return {"message": "product deleted"}, 200
  
  # @products_bp.arguments(ProductSchema)
  def put(self, product_id):
    request_data = request.get_json()
    product = ProductModel.query.get(product_id)
    if product:
      # product exists. update the values
      product.name = request_data["name"]
      if "price" in request_data:
        product.price = request_data["price"]
    else:
      # Product doesn't exist. Create a new product
      product = ProductModel(**request_data)
      
    db.session.add(product)
    db.session.commit()
    return product.getDict(), 201
    
    
    
    
  

    