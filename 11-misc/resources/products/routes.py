from flask_smorest import Blueprint
from flask.views import MethodView

# 11-misc
from flask import request, make_response

from db import db
from schemas import ProductSchema
from models.products import ProductModel
from models.reviews import ReviewModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, select
from ..utils import row2dict
# 09-auth
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from flask_jwt_extended import current_user

product_bp = Blueprint("products_blueprint", __name__, description="products bp")

# Get individual product.
# Model.query.get_or_404(product_id)
@product_bp.route("/products/<string:product_id>")
class Product(MethodView):
  @product_bp.response(200, ProductSchema)
  def get(self, product_id):
    try:
      product = ProductModel.query.get_or_404(product_id, "Product not found")
      return product
      # return row2dict(product)
    except SQLAlchemyError:
      return {"message": "Product not found"}, 404
  
  @product_bp.arguments(ProductSchema)
  @jwt_required()
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
      execQueries()
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
  @product_bp.response(201, ProductSchema)
  # 09-auth
  @jwt_required()
  def post(self, request_data):
    # insert into db.
    try:
      # 09-auth
      jwt = get_jwt()
      print(jwt)
      print(jwt["is_admin"])
      print(current_user.username)
        
      # pm = ProductModel(name=request_data["name"], price=request_data["price"])
      pm = ProductModel(**request_data)
      db.session.add(pm)
      db.session.commit()
      print(pm.id)
      
      # product_id = str(pm.id) #uuid.uuid4().hex
      # new_product = {product_id: {"name": request_data["name"], "price": request_data["price"]}}
      # products.update(new_product)
      return pm, 201
    except SQLAlchemyError:
      return {"message": "Could not insert new Product into DB"}, 500

@product_bp.route("/products/<string:product_id>/reviews")
class ReviewsForProduct(MethodView):
  def get(self, product_id):
    product = ProductModel.query.get_or_404(product_id)
    return [review.getDict() for review in product.reviews]

# 11-misc
# return xml response
# make_response used to customize the response
@product_bp.route("/products/xml")
class ProductListXMLView(MethodView):
  def get(self):
    try:
      products = ProductModel.query.all()
      ret = "<data>"
      for prod in products:
        ret += f'<product><id>{prod.id}</id><name>{prod.name}</name><price>{prod.price}</price></product>'
      ret += "</data>"
      # 11-misc
      # Flask provides a method called make_response() that we can use to send custom headers, 
      # as well as change the property (like status_code, mimetype, etc.) in response.
      r = make_response(ret)
      r.status_code=200
      r.mimetype="application/xml"
      r.headers["Content-Type"] = "text/xml; charset=utf-8"
      return r
    except SQLAlchemyError as e:
      return {"message": str(e)}, 500
  
# This method is written for demo purpose.
# Different types of queries - simple select, join, paginate, order by, raw query, etc
# Also, this method demonstrates how to process the results.
def execQueries():
  try:
    #######
    ### Simple query
    print("querying ProductModel")
    pm = ProductModel.query.filter_by(name="Android phone2").first()
    print(pm)
    ### End Simple query
    ### Order by
    print("Order by")
    pms = ProductModel.query.order_by(ProductModel.price).all()
    [print(pm.price, pm.name) for pm in pms]
    ### End Order by
    ### Simple join with relationship
    print("Simple join with relationship")
    result = ProductModel.query.add_columns(ReviewModel.review_text, ReviewModel.id).join(ProductModel.reviews).all()
    [print(res) for res in result]
    ### End simple join with relationship
    ### Join
    # Use select().join_from()
    stmt = select(ProductModel.id, ProductModel.name, ReviewModel.review_text).join_from(ProductModel, ReviewModel)
    print(stmt)
    # session.execute returns an iterable of tuples. 
    # Number of values in a tuple will be the number of columns in the result
    results = db.session.execute(stmt)
    for res in results:
      print(res[0], res[1])
    ### End Join
    ### Pagination.
    # Use query.paginate
    rs = ReviewModel.query.paginate(page=1,per_page=5,error_out=False)
    for r in rs:
      print(r.review_text)
    ### End Pagination
    ### Or, and
    stmt2 = ProductModel.query.filter((ProductModel.price > 20000) | (ProductModel.id == 1))
    print(stmt2)
    # session.execute returns an iterable of tuples. 
    # Number of values in a tuple will be the number of columns in the result
    results = db.session.execute(stmt2)
    for r in results:
      print(r[0])
    ### End Or, and
    ### Raw query
    print("Raw query")
    stmt3 = text('select * from products where price < 25000')
    result = db.session.execute(stmt3)
    [print(row) for row in result]
    ### End Raw query
    ### Using the where clause along with select
    print("Where clause with select")
    stmt = select(ProductModel).where(ProductModel.name != "Android phone1" and ProductModel.price > 20000)
    print(stmt)
    # pms = db.session.scalars(stmt).all()
    pms = db.session.execute(stmt)
    for pm in pms:
      print(pm[0].id, pm[0].name)
    ### End Using the where clause along with select
    #######
  except SQLAlchemyError as e:
    print(str(e))