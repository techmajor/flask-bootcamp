from flask import Flask, request
from db import db
import uuid
from resources.products.routes import products_bp
from resources.reviews.routes import reviews_bp
from resources.tags.routes import tags_bp

app = Flask(__name__)
app.register_blueprint(products_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(tags_bp)

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

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = connection_str

# init SQLAlchemy
db.init_app(app)

# import all models and then create_all()
from models.Products import ProductModel
from models.Reviews import ReviewModel
from models.Tags import TagModel
from models.ProductsTags import ProductsTagsModel

with app.app_context():
    db.create_all()