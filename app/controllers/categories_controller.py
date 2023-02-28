from app import db
from app.models.categories_model import CategoryModel
from app.schemas.categories_schema import CategoriesResponseSchema

class CategoriesController:
    def __init__(self):
        self.model = CategoryModel
        self.schema = CategoriesResponseSchema

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
                'message': f'La categoria {data["name"]} se creo con exito'
            }, 201

        except Exception as e:
            db.session.rollback()
            return{
                'message': 'Ocurrio un error',
                'error': str(e)
            },500
    
    def getbyid(self, id):
        try:
            record = self.model.where(id=id).first()
            if record:
                response = self.schema(many=False)
                return response.dump(record), 200
            return {
                'message': 'No se encontro el rol mencionado'
            }, 404
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
        
        