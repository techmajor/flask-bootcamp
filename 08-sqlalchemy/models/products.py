from db import db

class ProductModel(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  price = db.Column(db.Integer, nullable=False)
  reviews = db.relationship("ReviewModel", back_populates="product", cascade="all, delete")
  
  tags = db.relationship("TagModel", back_populates="products", secondary="products_tags")
  
  def getDict(self):
    return {"id": self.id, "name": self.name, "price": self.price}