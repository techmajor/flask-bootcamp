from db import db
# 09-auth
# User model to store username, password and the user ID.
# Store password as a hash. Never plain text.
class UserModel(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(500), nullable=False)
  
  # 09-auth
  # DO NOT return password.
  def getDict(self):
    return { "username": self.username, "id": self.id }