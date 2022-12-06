from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from flask import request
from schema import TagSchema, ProductIdSchema, ProductSchema

from models.Products import ProductModel
from models.Tags import TagModel
from models.ProductsTags import ProductsTagsModel
from models.utils import row2Dict
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint
tags_bp = Blueprint("Tags", __name__, description="Operations on tags")

# APIs for tags
# 1. Create a tag
# 2. Get tag by id
# 3. Get tags by product id
# 4. Update tag by id
# 5. Delete tag by id
# 6. Get all tags
# 7. Add product to a tag
# 8. Remove product from a tag
# 9. Get products by tag id

# Associate routes
@tags_bp.route("/tags")
class TagListView(MethodView):
  # 1. Create a tag
  @tags_bp.arguments(TagSchema)
  def post(self, request_data):
    try:
      tag = TagModel(**request_data)
      db.session.add(tag)
      db.session.commit()
      return tag.getDict()
    except SQLAlchemyError as e:
      return {"message": str(e)}, 401
  
  # 6. Get all tags
  def get(self):
    try:
      tags = TagModel.query.order_by(TagModel.name).all() 
      return [tag.getDict() for tag in tags]
    except SQLAlchemyError as e:
      return {"message": str(e)}, 401
    
@tags_bp.route("/tags/<int:tag_id>")
class TagView(MethodView):
  # 2. Get tag by id
  def get(self, tag_id):
    try:
      tag = TagModel.query.get_or_404(tag_id)
      return tag.getDict()
    except SQLAlchemyError as e:
      return {"message": str(e)}
  
  # 5. Delete tag by id
  def delete(self, tag_id):
    try:
      tag = TagModel.query.get_or_404(tag_id)
      if not tag.products:
        # No products associated with the tag
        # So, we can delete
        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag deleted"}, 200
      return {"message": "Tag cannot be deleted."}, 400
    except SQLAlchemyError as e:
      return {"message": str(e)}
    
@tags_bp.route("/tags/<int:tag_id>/products")
class Tag2ProductMappingView(MethodView):
  # 9. Get products by tag id
  @tags_bp.response(200, ProductSchema(many = True))
  def get(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    return tag.products
  
  # 7. Add product to a tag
  @tags_bp.arguments(ProductIdSchema)
  def post(self, request_data, tag_id):
    try:
      tag = TagModel.query.get_or_404(tag_id)
      product = ProductModel.query.get_or_404(request_data["product_id"])
      # Tag and Product exist
      # Approach 1
      # prods_tags = ProductsTagsModel(tag_id=tag.id, product_id=product.id)
      # db.session.add(prods_tags)
      # db.session.commit()
      # Approach 2
      tag.products.append(product)
      db.session.add(tag)
      db.session.commit()
      
      return [prod.getDict() for prod in tag.products]
    except SQLAlchemyError as e:
      return {"message": str(e)}
    
    

