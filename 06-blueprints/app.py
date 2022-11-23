from flask import Flask
from products.routes import product_bp
from reviews.routes import reviews_bp

app = Flask(__name__)

# Register blueprints with app
app.register_blueprint(product_bp)
app.register_blueprint(reviews_bp)

@app.get("/")
def get_hello():
  return "hello world"
