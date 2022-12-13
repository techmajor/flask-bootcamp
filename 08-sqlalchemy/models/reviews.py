from db import db

class ReviewModel(db.Model):
  __tablename__ = "reviews"
  id = db.Column(db.Integer, primary_key=True)
  review_text = db.Column(db.String(200), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
  product = db.relationship("ProductModel", back_populates="reviews")
  
  def getDict(self):
    return { "id": self.id,
            "review_text": self.review_text,
            "product_id": self.product_id
            }