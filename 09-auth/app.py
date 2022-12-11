from flask import Flask, jsonify
from db import db
import uuid
from resources.products.routes import product_bp
from resources.reviews.routes import reviews_bp
from resources.tags.routes import tags_bp
from resources.users.routes import users_bp

from flask_sqlalchemy import SQLAlchemy
# 09-auth
from flask_jwt_extended import JWTManager

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'database': 'test_db'
}
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

def create_app():
  app = Flask(__name__)

  # Register blueprints
  app.register_blueprint(product_bp)
  app.register_blueprint(reviews_bp)
  app.register_blueprint(tags_bp)
  app.register_blueprint(users_bp)
  
  # Configure SQLAlchemy
  app.config['SQLALCHEMY_DATABASE_URI'] = connection_str

  # init SQLAlchemy
  db.init_app(app)
  
  # 09-auth
  # init jwt
  app.config["JWT_SECRET_KEY"] = "techmajor-key"
  jwt = JWTManager(app)
  
  # 09-auth
  # jwt methods that can be overridden 

  # This method is called when the access token has expired.
  # The error message sent back can be configured here.
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message": "The token has expired", "error": "token_error"}), 
            401)
  
  # This method is called when the access token is invalid.
  # The error message sent back can be configured here.
  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (jsonify({"message": "Your token is not valid", "error": "invalid_token"}), 
            401)
  
  # This method is called when the access token is missing in the request.
  # The error message sent back can be configured here.
  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return (jsonify({"desc": "No access token in request", "error": "auth_error"}),
            401)
  
  # Using the additional_claims_loader, we can specify a method that will be
  # called when creating JWTs. The decorated method must take the identity
  # we are creating a token for and return a dictionary of additional
  # claims to add to the JWT.
  # https://flask-jwt-extended.readthedocs.io/en/stable/add_custom_data_claims/
  @jwt.additional_claims_loader
  def add_claims_callback(identity):
    if identity == 1 or identity == 2:
      return {"is_admin": True}
    return {"is_admin": False}

  # jwt methods end.

  # import all models and then create_all()
  from models.products import ProductModel
  from models.reviews import ReviewModel
  from models.tags import TagModel
  from models.products_tags import ProductTagModel
  from models.users import UserModel

  with app.app_context():
      db.create_all()

  return app
