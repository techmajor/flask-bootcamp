from flask_smorest import Blueprint
from flask import request
from flask.views import MethodView
import uuid
from db import reviews
from schemas import ReviewSchema

reviews_bp = Blueprint("reviews_blueprint", __name__, description="Reviews bp")

@reviews_bp.route("/reviews/<string:review_id>")
class Review(MethodView):
  def get(self, review_id):
    try:
      return reviews[review_id], 200
    except KeyError:
      return {"message": "review not found"}, 404
  
  # def put(self, review_id):

@reviews_bp.route("/reviews")
class ReviewList(MethodView):
  @reviews_bp.arguments(ReviewSchema)
  def post(self, request_data):
    # request_data = request.get_json()
    # Should have product_id, review_text
    # if("product_id" not in request_data 
    #    or "review_text" not in request_data):
    #   return {"message":"Bad request. No product_id or review_text"}, 400
    review_id = uuid.uuid4().hex
    reviews[review_id] = {"product_id": request_data["product_id"], "review_text": request_data["review_text"]}
    return {"message": "Review added"}, 201
  
  def get(self):
    # return list(reviews.values()), 200
    return reviews, 200