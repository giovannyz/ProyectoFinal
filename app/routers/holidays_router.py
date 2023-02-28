from app import api
from flask_restx import Resource
from app.schemas.holidays_schema import HolidaysRequestSchema
from app.controllers.holidays_controller import HolidayController

holiday_ns = api.namespace(
    name='Feriados',
    description='Rutas del modelo de feriados',
    path='/holidays'
)

request_parser = HolidaysRequestSchema(holiday_ns)

@holiday_ns.route('/')
class Holiday(Resource):
    @holiday_ns.expect(request_parser.all())
    def get(self):
        '''Listar todos los feriados'''
        query = request_parser.all().parse_args()
        controller = HolidayController()
        return controller.all(query)

    @holiday_ns.expect(request_parser.create(), validate=True)
    def post(self):
        '''Creacion de feriados'''
        controller = HolidayController()
        return controller.create(holiday_ns.payload)

@holiday_ns.route('/<int:id>')
class HolidayById(Resource):
    def get(self, id):
        '''Obtener un feriado por el id'''
        controller = HolidayController()
        return controller.getById(id)

    @holiday_ns.expect(request_parser.update(), validate=True)
    def put(self, id):
        '''Actualizar un feriado por el id'''
        controller = HolidayController()
        return controller.Update(id, holiday_ns.payload)

    def delete(self, id):
        '''Deshabilitar un feriado por el id'''
        controller = HolidayController()
        return controller.Delete(id)
    
@holiday_ns.route('/delivery_dates')
class DeliveryDates(Resource):
    def get(self):
        '''Listar todas las fechas de entrega disponibles'''
        controller = HolidayController()
        return controller.deliveryDate()
