from flask import Flask, request, Blueprint
from db import db
import uuid
from resources.products.routes import product_bp
from resources.reviews.routes import reviews_bp
from flask_sqlalchemy import SQLAlchemy

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
  
  # Configure SQLAlchemy
  app.config['SQLALCHEMY_DATABASE_URI'] = connection_str

  # init SQLAlchemy
  db.init_app(app)

  # import all models and then create_all()
  from models.products import ProductModel
  from models.reviews import ReviewModel

  with app.app_context():
      db.create_all()

  return app
