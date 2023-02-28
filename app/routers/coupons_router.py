from app import api
from app.schemas.coupons_schema import CouponsRequestSchema
from flask_restx import Resource
from app.controllers.coupons_controller import CouponsController

coupons_ns = api.namespace(
    name = 'coupons',
    description = 'Vista de rutas de Cupones',
    path='/coupons'
)

request_parser = CouponsRequestSchema(coupons_ns)

@coupons_ns.route('/')
class Coupons(Resource):
    @coupons_ns.expect(request_parser.all())
    def get(self):
        '''Listar los cupones'''
        query = request_parser.all().parse_args()
        controller = CouponsController()
        return controller.all(query)

    @coupons_ns.expect(request_parser.create(), validate=True)
    def post(self):
        '''Creacion de Cupones'''
        controller = CouponsController()
        return controller.create(coupons_ns.payload)

@coupons_ns.route('/<int:id>')
class CouponsById(Resource):

    def get(self, id):
        '''Traer un cupon por ID'''
        controller = CouponsController()
        return controller.getById(id)

    @coupons_ns.expect(request_parser.update(), validate=True)
    def put(self, id):
        '''Actualizar un cupon por ID'''
        controller = CouponsController()
        return controller.Update(id, coupons_ns.payload)

    def delete(self, id):
        '''Deshabilitar un cupon por ID'''
        controller = CouponsController()
        return controller.Delete(id)

