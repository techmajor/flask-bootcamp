from db import db

class DummyModel(db.Model):
  __tablename__ = "dummy"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), nullable=False, unique=True)
  description = db.Column(db.String(200), nullable=True)