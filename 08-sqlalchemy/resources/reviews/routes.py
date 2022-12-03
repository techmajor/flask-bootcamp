from flask_smorest import Blueprint
from flask import request
from flask.views import MethodView
from db import db
from models.reviews import ReviewModel
from schemas import ReviewSchema, EditReviewSchema
from ..utils import row2dict
from sqlalchemy.exc import SQLAlchemyError

reviews_bp = Blueprint("reviews_blueprint", __name__, description="Reviews bp")

@reviews_bp.route("/reviews/<string:review_id>")
class Review(MethodView):
  def get(self, review_id):
    review = ReviewModel.query.get_or_404(review_id)
    return review.getDict()
  
  @reviews_bp.arguments(EditReviewSchema)  
  def put(self, request_data, review_id):
    review = ReviewModel.query.get(review_id)
    if review:
      review.review_text = request_data["review_text"]
    else:
      review = ReviewModel(**request_data)
      
    db.session.add(review)
    db.session.commit()
    return review.getDict(), 201

@reviews_bp.route("/reviews")
class ReviewList(MethodView):
  @reviews_bp.arguments(ReviewSchema)
  def post(self, request_data):
    try:
      review = ReviewModel(**request_data)
      # review = ReviewModel(product_id=request_data["product_id"], review_text=request_data["review_text"])
      db.session.add(review)
      db.session.commit()
      print("Review added: " + str(review.id))
      return review.getDict(), 201
    except SQLAlchemyError as e:
      return {"message": "DB error while adding review"}
  
  def get(self):
    reviews = ReviewModel.query.all()
    reviews_list = []
    for review in reviews:
      r = review.getDict()
      print(review.product.name)
      r.update({"name": review.product.name})
      reviews_list.append(r)
      
    # return [review.getDict() for review in reviews], 200
    return reviews_list, 200
    