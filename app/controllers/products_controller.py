from app import db
from app.models.products_model import ProductsModel
from app.schemas.products_schema import ProductsResponseSchema
from sqlalchemy import or_

class ProductsController:
    def __init__(self):
        self.model = ProductsModel
        self.schema = ProductsResponseSchema
    
    def all(self, query):
        try:
            filters = {}

            page = query['page']
            per_page = query['per_page']

            if query['q']:
                filters = {
                    or_: {
                        'name__ilike': f"%{query['q']}%",
                        'description__ilike': f"%{query['q']}%"
                    }
                }

            if query['category_id']:
                filters['category_id'] = query['category_id']

            if query['status'] is not None:
                filters['status'] = bool(query['status'])

            ordering = query['ordering'].split(
                ',') if query['ordering'] else ['id']

            records = self.model.smart_query(
                filters={**filters},
                sort_attrs=ordering
            ).paginate(
                page=page, per_page=per_page
            )

            response = self.schema(many=True)
            return {
                'results': response.dump(records.items),
                'pagination': {
                    'totalRecords': records.total,
                    'totalPages': records.pages,
                    'perPage': records.per_page,
                    'currentPage': records.page
                }
            }, 200
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
        
    def create(self, data):
        try:
            new_record = self.model.create(**data)
            db.session.add(new_record)
            db.session.commit()

            return {
                'message': f'El producto {data["name"]} se creo con exito'
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
        
    def getById(self, id):
        try:
            record = self.model.where(id=id).first()
            if record:
                response = self.schema(many=False)
                return response.dump(record), 200
            return {
                'message': 'No se encontro el producto mencionado'
            }, 404
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
        
    def update(self,id, data):
        try:
            record = self.model.where(id=id).first()
            if record:
                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'El producto {id}, ha sido actualizada'
                }, 200
            return {
                'message': 'No se encontro el producto mencionado'
            }, 404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500


    def delete(self, id):
        try:
            record = self.model.where(id=id).first()
            if record and record.status:
                record.update(status=False)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'El producto {id}, ha sido deshabilitada'
                }, 200
            return {
                'message': 'No se encontro el producto mencionado'
            }, 404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
    

    def _reduceStockToProducts(self, items):
        updates = []

        for item in items:
            record = self.model.where(id=item.product_id).first()
            new_stock = record.stock - item.quantity
            record.update(stock=new_stock)
            updates.append(record)

        return updates