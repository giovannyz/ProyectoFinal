from app import api
from flask_restx import Resource
from flask_jwt_extended import jwt_required
#from app.schemas.orders_schemas import OrderRequestSchema
#from app.controllers.orders_controller import OrderController

pedido_ns = api.namespace(
    name='Ordenes de Compra',
    description='Rutas para el modelo de Ordenes',
    path='/orders'
)

#request_schema = OrderRequestSchema(pedido_ns)


@pedido_ns.route('')
class Pedido(Resource):
    
    def post(self):
        ''' Creación de un pedido '''
        pass