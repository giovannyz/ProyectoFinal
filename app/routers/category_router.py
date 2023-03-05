from app import api
from flask import request
from flask_restx import Resource
from app.controllers.category_controller import CategoryController
from app.schemas.category_schemas import CategoryRequestSchema
from flask_jwt_extended import jwt_required

category_ns = api.namespace(
    name='Categoria',
    description='Rutas del modelo de Categoria',
    path='/categoria'
)

request_schema = CategoryRequestSchema(category_ns)

@category_ns.doc(security='Bearer')
@category_ns.route('')
class Category(Resource):
    @jwt_required()
    @category_ns.expect(request_schema.all())
    def get(self):
        '''Listar Categoria'''
        query = request_schema.all().parse_args()
        controller = CategoryController()
        return controller.all(query)

    @jwt_required()
    @category_ns.expect(request_schema.create(), validate=True)
    def post(self):
        '''Creacion de Categoria'''
        controller = CategoryController()
        return controller.create(request.json)

@category_ns.doc(security='Bearer')
@category_ns.route('/<int:id>')
class CategoryById(Resource):
    @jwt_required()
    def get(self, id):
        '''Traer categoria por id'''
        controller = CategoryController()
        return controller.getById(id)

    @jwt_required()
    @category_ns.expect(request_schema.update(), validate=True)
    def put(self, id):
        '''Actualizar categoria'''
        controller = CategoryController()
        return controller.update(id, request.json)

    @jwt_required()
    def delete(self,id):
        '''Deshabilitar por id'''
        controller = CategoryController()
        return controller.delete(id)
