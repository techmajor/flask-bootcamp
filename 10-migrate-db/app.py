from flask import Flask, jsonify
from db import db
import uuid
from resources.products.routes import product_bp
from resources.reviews.routes import reviews_bp
from resources.tags.routes import tags_bp
from resources.users.routes import users_bp

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# 10-migrate-db
from flask_migrate import Migrate

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
  
  # init jwt
  app.config["JWT_SECRET_KEY"] = "techmajor-key"
  jwt = JWTManager(app)
  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message": "The token has expired", "error": "token_error"}), 
            401)
  
  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (jsonify({"message": "Your token is not valid", "error": "invalid_token"}), 
            401)
  
  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return (jsonify({"desc": "No access token in request", "error": "auth_error"}),
            401)
  
  @jwt.additional_claims_loader
  def add_claims_callback(identity):
    if identity == 1 or identity == 2:
      return {"is_admin": True}
    return {"is_admin": False}

  # import all models and then create_all()
  from models.products import ProductModel
  from models.reviews import ReviewModel
  from models.tags import TagModel
  from models.products_tags import ProductTagModel
  from models.users import UserModel
  from models.dummy import DummyModel
  
  # 10-migrate-db
  migrate = Migrate(app, db)

  # with app.app_context():
  #     db.create_all()

  return app
