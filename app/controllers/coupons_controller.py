from app import db
from app.models.coupons_model import CouponModel
from app.schemas.coupons_schema import CouponsResponseSchema

class CouponsController:
    def __init__(self):
        self.model = CouponModel
        self.schema = CouponsResponseSchema
    
    def all(self, query):
        try:
            page = query['page']
            per_page = query['per_page']

            records = self.model.where(status=True).order_by('id').paginate(page=page, per_page=per_page)
            
            response = self.schema(many=True)
            return {
                'results': response.dump(records.items),
                'pagination': {
                    'TotalRecords': records.total,
                    'TotalPages': records.page,
                    'perPage': records.per_page,
                    'currentPage': records.page
                }
            }, 200

        except Exception as e:
            db.session.rollback()
            return{
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
    def create(self, data):
        try:
            new_record = self.model.create(**data)
            db.session.add(new_record)
            db.session.commit()
            return {
                'message': f'El cupon {data["code"]} se creo con exito'
            }, 201

        except Exception as e:
            db.session.rollback()
            return{
                'message': 'Ocurrio un error',
                'error': str(e)
            },500
    
    def getById(self, id):
        try:
            record = self.model.where(id=id).first()
            if record:
                response = self.schema(many=False)
                return response.dump(record), 200
            return {
                'message': 'No se encontro el cupon mencionado'
            }, 404
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def Update(self, id, data):
        try:
            record = self.model.where(id=id).first()
            if record:
                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'El cupon {id}, ha sido actualizado'
                }, 200
            return {
                'message': 'No se encontro el cupon mencionado'
            }, 404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500


    def Delete(self, id):
        try:
            record = self.model.where(id=id).first()
            if record and record.status:
                record.update(status=False)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'El Cupon {id}, ha sido deshabilitado'
                }, 200
            return {
                'message': 'No se encontro el Cupon mencionado'
            }, 404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500