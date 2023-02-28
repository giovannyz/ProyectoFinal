from app import api
from flask import request
from flask_restx import Resource
from app.schemas.categories_schema import CategoriesRequestSchema
from app.controllers.categories_controller import CategoriesController

category_ns = api.namespace(
    name = 'Categorias de Producto',
    description = 'Rutas del modelo de Categorias',
    path = '/categories'
)

request_schema = CategoriesRequestSchema(category_ns)

@category_ns.route('/')
class CategoryRouter(Resource):
    @category_ns.expect(request_schema.all())
    def get(self):
        '''Listar todas las categorias'''
        query = request_schema.all().parse_args()
        controller = CategoriesController()
        return controller.all(query)

    @category_ns.expect(request_schema.create(), validate=True)
    def post(self):
        '''Creacion de Categorias'''
        controller = CategoriesController()
        return controller.create(request.json)

@category_ns.route('/<int:id>')
class CategoryById(Resource):
    def get(self, id):
        '''Obtener una categoria por id'''
        controller = CategoriesController()
        return controller.getbyid(id)
    
    
