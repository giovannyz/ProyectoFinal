from app import db
from app.models.shopping_cart_model import ShoppingCartModel
from app.schemas.shopping_cart_schemas import ShoppingCartResponseSchema
from flask_jwt_extended import current_user

class ShoppingCartController:
    def __init__(self):
        self.model = ShoppingCartModel
        self.user_id = current_user.id
        self.schema = ShoppingCartResponseSchema
        self.precioTotal=0
    
    def all(self):
        try:
            return self._getAllProducts(self.user_id), 200
        except Exception as e:
            return {
                'message': 'Ocurrio un error de jean',
                'error': str(e)
            }, 500

    def update(self, data):

        try:
            record = self.model.where(
                user_id=self.user_id,
                product_id=data['product_id']
            ).first()

            if record:
                record.update(**data)
            else:
                data['user_id'] = self.user_id
                record = self.model.create(**data)

            db.session.add(record)
            db.session.commit()

            return {
                'message': 'Se actualizo el carrito de compras'
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
    
    def delete(self, id):
        try:
            record = self.model.where(
                user_id=self.user_id,
                product_id=id
            ).first()

            if record:
                record.delete()
                db.session.commit()

                return {
                    'message': 'Se elimino el producto con exito'
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

    def _getAllProducts(self, user_id):
        records = self.model.where(user_id=user_id).all()
        response = self.schema(many=True)
        data = response.dump(records)

        if records:
            for item in data:
                precio = item['product']['precio']
                quantity = item['quantity']
                self.precioTotal += precio * quantity
        return {
            'data': data,
            'precio Total': self.precioTotal
        }
