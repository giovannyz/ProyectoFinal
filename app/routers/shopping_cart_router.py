from app import api
from flask_restx import Resource
from app.schemas.shopping_cart_schemas import ShoppingCartRequestSchema
from app.controllers.shopping_cart_controller import ShoppingCartController
from flask_jwt_extended import jwt_required


shopping_ns = api.namespace(
    name='carrito de compras',
    description='Vista de carrito de compras',
    path='/shoppingCart'
)

request_schema = ShoppingCartRequestSchema(shopping_ns)

@shopping_ns.doc(security='Bearer')
@shopping_ns.route('')
class Shopping_cart(Resource):
    @jwt_required()
    def get(self):
        '''Listar carrito de compras'''
        controller = ShoppingCartController()
        return controller.all()
    @jwt_required()
    @shopping_ns.expect(request_schema.update(), validate=True)
    def put(self):
        '''Crear o Editar carrito de compras'''       
        controller = ShoppingCartController()
        return controller.update(shopping_ns.payload)

@shopping_ns.doc(security='Bearer')
@shopping_ns.route('/<int:product_id>')
class ShoppingCartById(Resource):
    @jwt_required()
    def delete(self, product_id):
        '''Inhabilitar producto de carrito'''
        controller = ShoppingCartController()
        return controller.delete(product_id)