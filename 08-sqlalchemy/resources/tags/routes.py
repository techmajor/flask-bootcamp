from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from db import db
from sqlalchemy.exc import SQLAlchemyError

from models.tags import TagModel
from models.products_tags import ProductTagModel
from models.products import ProductModel

from schemas import TagSchema, ErrorSchema, Product2TagSchema


# Create Blueprint
tags_bp = Blueprint("tags_blueprint", __name__, description="Tags bp")

# Associate blueprint with routes and define view functions

### Operations on tags
# 1. Create a tag
# 2. Add a product to a tag
# 3. Remove product from tag
# 4. List products for a tag
# 5. List tags
# 6. Edit a tag
# 7. Delete a tag
###

@tags_bp.route("/tags")
class TagView(MethodView):
  # List tags.
  @tags_bp.response(200, TagSchema(many=True))
  def get(self):
    return TagModel.query.order_by(TagModel.id).all()
  
  # Create a tag
  @tags_bp.arguments(TagSchema)
  def post(self, request_data):
    try:
      tag = TagModel(**request_data)
      db.session.add(tag)
      db.session.commit()
      return tag.getDict(), 201
    except SQLAlchemyError as e:
      return {"message": str(e)}, 500

@tags_bp.route("/tags/<int:tag_id>")
class TagProductView(MethodView):
  # Get Products for a tag
  def get(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    return [p.getDict() for p in tag.products]
  
  # Add product to a tag
  @tags_bp.arguments(Product2TagSchema)
  def post(self, request_data, tag_id):
    try:
      product_id = request_data["product_id"]
      # Make sure the product and tag exist
      prod = ProductModel.query.get_or_404(product_id)
      tag = TagModel.query.get_or_404(tag_id)
      # prod_tag = ProductTagModel(**request_data)
      # prod_tag.tag_id = tag_id
      # db.session.add(prod_tag)
      prod.tags.append(tag)
      db.session.add(prod)
      db.session.commit()
      return [p.getDict() for p in tag.products], 201
    except SQLAlchemyError as e:
      return {"message": str(e)}, 500
  
  def delete(self, tag_id):
    try:
      tag = TagModel.query.get_or_404(tag_id)
      db.session.delete(tag)
      db.session.commit()
      return {"message": "Tag deleted"}, 200
    except SQLAlchemyError as e:
      return {"message": str(e)}, 500
    