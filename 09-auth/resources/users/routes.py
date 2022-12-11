from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import UserSchema
from models.users import UserModel
# 09-auth
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from datetime import timedelta
from passlib.hash import pbkdf2_sha256

users_bp = Blueprint("Users Blueprint", __name__, description="Users bp")

@users_bp.route("/users/register")
class UserRegister(MethodView):
  @users_bp.arguments(UserSchema)
  def post(self, request_data):
    try:
      # 09-auth
      # 1. Create User model
      # 2. Password to be hashed and stored. Plain password not to be stored.
      user = UserModel(
        username=request_data["username"],
        password=pbkdf2_sha256.hash(request_data["password"])
        )
      print("password: " + user.password)
      db.session.add(user)
      db.session.commit()
      return {"message": "User registered"}, 201
    except SQLAlchemyError as e:
      return {"message": str(e)}, 500
    
@users_bp.route("/users/<int:user_id>")
class User(MethodView):
  @jwt_required()
  def get(self, user_id):
    user = UserModel.query.get_or_404(user_id)
    return user.getDict()
  
  def delete(self, user_id):
    user = UserModel.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}
  
# 09-auth
@users_bp.route("/users/login")
class UserLogin(MethodView):
  @users_bp.arguments(UserSchema)
  def post(self, request_data):
    user = UserModel.query.filter(
        UserModel.username == request_data["username"]
      ).first()
    if user and pbkdf2_sha256.verify(request_data["password"], user.password):
      access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
      return {"access_token": access_token}, 200
    return {"message": "Invalid credentials"}