from db import db

class ProductsTagsModel(db.Model):
  __tablename__ = "products_tags"
  id = db.Column(db.Integer, primary_key=True)
  product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
  tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
  
  unq_cons = db.UniqueConstraint(product_id, tag_id, name="unq_1")
  
  