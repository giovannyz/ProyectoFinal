from app import db
from app.models.pedido_model import PedidoModel
from app.models.pedido_item_model import PedidoItemModel
from app.controllers.shopping_cart_controller import ShoppingCartController
from app.controllers.products_controller import ProductsController
from flask_jwt_extended import current_user

class PedidoController:
    def __init__(self):
        self.model = PedidoModel
        self.model_item = PedidoItemModel
        self.user_id = current_user.id

        self.shopping_cart = ShoppingCartController()
        self.product = ProductsController()

    def create(self, data):
        try:
            date_shipping = data.get('date_shipping')
            shopping_cart = self.shopping_cart._getAllProducts(self.user_id)
            products = shopping_cart['data']
            precio = shopping_cart['precioTotal']

            # Validar que existan productos en el carrito
            if not len(products):
                raise Exception('El carrito de compras esta vacio')

            # Creación del pedido
            pedido = self.model.create(
                user_id=self.user_id,
                total_price=precio,
                date_shipping=date_shipping
            )

            # Creación de detalle del pedido
            pedido_items = [
                self.model_item.create(
                    pedido_id=pedido.id,
                    product_id=item['product']['id'],
                    price=item['product']['precio'],
                    quantity=item['quantity']
                )
                for item in products
            ]

            # Reducir stock de los productos
            reduces = self.product._reduceStockToProducts(pedido_items)

            # Limpiar el carrito de compras
            shopping_cart_user = self.shopping_cart._deleteShoppingCartToUser(
                self.user_id
            )

            # Guardar el pedido y su detalle
            db.session.add(pedido)
            db.session.add_all(pedido_items)

            # Guardar o actualizar la reducción de stock
            db.session.add_all(reduces)

            # Guardar la limpieza del carrito de compras
            for shop_cart in shopping_cart_user:
                db.session.delete(shop_cart)

            # Ejecutar los cambios en la BD
            db.session.commit()

            return {
                'message': 'Se creo el pedido con exito'
            }, 200
        
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error de mrda',
                'error': str(e)
            }, 500

  