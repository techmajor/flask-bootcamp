from db import db

class TagModel(db.Model):
  __tablename__ = "tags"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False, unique=True)
  
  products = db.relationship("ProductModel", back_populates="tags", secondary="products_tags")
  
  
  def getDict(self):
    return {"id": self.id, "name": self.name}