from marshmallow import Schema, fields

class ProductSchema(Schema):
  # id = fields.Str(dump_only=True)
  name = fields.Str(required=True)
  price = fields.Int(required=True)

class ReviewSchema(Schema):
  # id = fields.Str(dump_only=True)
  product_id = fields.Str(required=True)
  review_text = fields.Str(required=True)
  
class ProductRatingSchema(Schema):
  rating = fields.Int(required=True)
  opt_field = fields.Str() # Optional field.

class RatingsResponseSchema(Schema):
  ratings = fields.List(fields.Int, many=True)

  