from marshmallow import Schema, fields

class ProductSchema(Schema):
  name = fields.Str(required=True)
  price = fields.Int(required=True)
  id = fields.Str(dump_only=True)
  
class ProductRatingsSchema(Schema):
  ratings = fields.Int(required=True)
  
class RatingsResponseSchema(Schema):
  ratings = fields.List(fields.Int)
  abcd = fields.Str(required=True)
  
class TagSchema(Schema):
  name = fields.Str(required=True)

class ProductIdSchema(Schema):
  product_id = fields.Int(required=True)
  