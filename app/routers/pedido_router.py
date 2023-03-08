from app import api
from flask_restx import Resource
from app.schemas.pedido_schemas import PedidoRequestSchema
from app.controllers.pedido_controller import PedidoController
from flask_jwt_extended import jwt_required

pedido_ns = api.namespace(
    name='Pedidos',
    description='Rutas de pedidos',
    path='/pedido'
)

request_schema = PedidoRequestSchema(pedido_ns)

@pedido_ns.doc(security='Bearer')
@pedido_ns.route('')
class Pedido(Resource):
    @jwt_required()
    @pedido_ns.expect(request_schema.create(), validate=True)
    def post(self):
        '''Creacion de pedido'''
        controller = PedidoController()
        return controller.create(pedido_ns.payload)