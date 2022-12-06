from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from models.Reviews import ReviewModel
from models.Products import ProductModel


reviews_bp = Blueprint("Reviews", __name__, description="Operations on reviews")

@reviews_bp.route("/reviews/<string:review_id>")
@reviews_bp.route("/reviews/<string:review_id>/")
class ReviewView(MethodView):
  def get(self, review_id):
    try:
      review = ReviewModel.query.get_or_404(review_id)
      return review.getDict(), 200
    except SQLAlchemyError:
      return {"message": "Review not found"}

@reviews_bp.route("/reviews")
@reviews_bp.route("/reviews/")
class ReviewListView(MethodView):
  def get(self):
    
    reviews = ReviewModel.query.all()
    return [review.getDict() for review in reviews], 200

@reviews_bp.route("/products/<string:product_id>/reviews")
class ProductReviewView(MethodView):
  def get(self, product_id):
    try:
      product = ProductModel.query.get_or_404(product_id)
      return [review.getDict() for review in product.reviews]
    except SQLAlchemyError:
      return {"message": "DB error"}, 404

  def post(self, product_id):
    try:
      request_data = request.get_json()
      # 1. Create a ReviewModel
      review = ReviewModel(**request_data)
      review.product_id = product_id
      db.session.add(review)
      db.session.commit()
      
      print(review.product.name)
      return review.getDict(), 201
    except SQLAlchemyError:
      return {"message": "Product not found"}, 404