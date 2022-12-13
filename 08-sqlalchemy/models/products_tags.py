from db import db

class ProductTagModel(db.Model):
  __tablename__ = "products_tags"
  id = db.Column(db.Integer, primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey("tags.id",ondelete="CASCADE"), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey("products.id",ondelete="CASCADE"), nullable=False)
  
  uc = db.UniqueConstraint(tag_id, product_id, name="unq_1")