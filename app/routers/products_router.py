from app import api
from flask import request
from flask_restx import Resource
from app.controllers.products_controller import ProductsController
from app.schemas.products_schema import ProductRequestSchema
from flask_jwt_extended import jwt_required

products_ns = api.namespace(
    name = 'Productos',
    description = 'Rutas de Productos',
    path = '/productos'
)

request_schema = ProductRequestSchema(products_ns)

@products_ns.doc(security='Bearer')
@products_ns.route('')
class Products(Resource):
    @jwt_required()
    @products_ns.expect(request_schema.all())
    def get(self):
        '''Listado de Productos'''
        query = request_schema.all().parse_args()
        controller = ProductsController()
        return controller.all(query)

    @jwt_required()
    @products_ns.expect(request_schema.create(), validate=True)
    def post(self):
        '''Creacion de Productos'''
        data = request_schema.create().parse_args()
        controller = ProductsController()
        return controller.create(data)

@products_ns.doc(security='Bearer')
@products_ns.route('/<int:id>')
class ProductsById(Resource):
    @jwt_required()
    def get(self, id):
        '''Traer Producto por ID'''
        controller = ProductsController()
        return controller.getById(id)
    
    @jwt_required()
    @products_ns.expect(request_schema.update(), validate=True)
    def put(self, id):
        '''Actualizar producto'''
        data = request_schema.update().parse_args()
        controller = ProductsController()
        return controller.update(id, data)
    
    @jwt_required()
    def delete(self, id):
        '''Inhabilitar Producto'''
        controller = ProductsController()
        return controller.delete(id)