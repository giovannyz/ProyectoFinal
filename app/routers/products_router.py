from app import api
from flask import request
from flask_restx import Resource
#from app.controllers.category_controller import CategoryController
#from app.schemas.category_schemas import CategoryRequestSchema
from flask_jwt_extended import jwt_required

products_ns = api.namespace(
    name = 'Productos',
    description = 'Rutas de Productos',
    path = '/productos'
)

@products_ns.route('')
class Products(Resource):
    def get(self):
        '''Listado de Productos'''
        pass
    def post(self, query):
        '''Creacion de Productos'''
        pass
@products_ns.route('/<int:id>')
class ProductsById(Resource):
    def get(self, id):
        '''Traer Producto por ID'''
        pass
    def put(self, id):
        '''Actualizar producto'''
        pass
    def delete(self, id):
        '''Inhabilitar Producto'''
        pass