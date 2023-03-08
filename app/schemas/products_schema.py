from flask_restx import fields
from flask_restx.reqparse import RequestParser
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from app.models.products_model import ProductsModel

class ProductRequestSchema:
    def __init__(self, namespace):
        self.namespace = namespace
    
    def all(self):
        parser = RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('q', type=str, required=False, location='args')
        parser.add_argument('category_id', type=int,
                            required=False, location='args')
        parser.add_argument('status', type=int,
                            required=False, location='args')
        parser.add_argument('ordering', type=str,
                            required=False, location='args')
        return parser
    
    def create(self):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True, location='form')
        parser.add_argument('description', type=str,
                            required=True, location='form')
        parser.add_argument('precio', type=float,
                            required=True, location='form')
        parser.add_argument('stock', type=int, required=True, location='form')
        parser.add_argument('cat_id', type=int,
                            required=True, location='form')
        return parser
    
    def update(self):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=False, location='form')
        parser.add_argument('description', type=str,
                            required=False, location='form')
        parser.add_argument('precio', type=float,
                            required=False, location='form')
        parser.add_argument('stock', type=int, required=False, location='form')
        parser.add_argument('cat_id', type=int,
                            required=False, location='form')
        return parser

    
class ProductsResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductsModel
        ordered = True
    
    category = Nested('CategoryResponseSchema', many=False)
        