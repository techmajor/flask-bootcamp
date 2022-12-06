from db import db

class ProductModel(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  price = db.Column(db.Integer, nullable=False)
  reviews = db.relationship("ReviewModel", back_populates="product")
  
  tags = db.relationship("TagModel", back_populates="products", secondary="products_tags")
  
  def getDict(self):
    return {
      "name": self.name,
      "price": self.price,
      "id": self.id
    }