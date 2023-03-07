from app import db
from app.models.pedido_model import PedidoModel
from app.models.pedido_item_model import PedidoItemModel

from app.controllers.products_controller import ProductsController
from flask_jwt_extended import current_user


class OrderController:
    def __init__(self):
        self.model = PedidoModel
        self.model_item = PedidoItemModel
        self.user_id = current_user.id

        self.product = ProductsController()
    

    def create(self, data):
        try:
            coupon = data.get('coupon')
            date_shipping = data.get('date_shipping')
            shopping_cart = self.shopping_cart._getAllProducts(self.user_id)
            products = shopping_cart['data']
            prices = shopping_cart['prices']
            prices['discount'] = 0

            # Validar que existan productos en el carrito
            if not len(products):
                raise Exception('El carrito de compras esta vacio')

            # Validar que el cupon exista y este dentro del rango de tiempo de uso
            # Recalcular precios si hubiera un descuento
            if coupon:
                percentage = self.coupon._validateDateTimeCouponToOrder(coupon)
                prices['discount'] = 0 if percentage is None else round(
                    prices['total'] * (percentage / 100), 2
                )
                prices['total'] = round(
                    prices['total'] - prices['discount'], 2
                )

            # Creación del pedido
            order = self.model.create(
                user_id=self.user_id,
                total_price=prices['total'],
                subtotal_price=prices['subtotal'],
                igv_price=prices['igv'],
                discount_price=prices['discount'],
                code_coupon=coupon,
                date_shipping=date_shipping
            )

            # Creación de detalle del pedido
            order_items = [
                self.model_item.create(
                    order_id=order.id,
                    product_id=item['product']['id'],
                    price=item['product']['price'],
                    quantity=item['quantity']
                )
                for item in products
            ]

            # Crear la URL de pago
            payment = self.__createPaymentUrl(order, products)
            payment_url = payment['init_point']

            order.checkout_id = payment['id']
            order.checkout_url = payment_url

            # Reducir stock de los productos
            reduces = self.product._reduceStockToProducts(order_items)

            # Limpiar el carrito de compras
            shopping_cart_user = self.shopping_cart._deleteShoppingCartToUser(
                self.user_id
            )

            # Guardar el pedido y su detalle
            db.session.add(order)
            db.session.add_all(order_items)

            # Guardar o actualizar la reducción de stock
            db.session.add_all(reduces)

            # Guardar la limpieza del carrito de compras
            for shop_cart in shopping_cart_user:
                db.session.delete(shop_cart)

            # Ejecutar los cambios en la BD
            db.session.commit()

            return {
                'message': 'Se creo el pedido con exito',
                'data': {
                    'checkout_url': payment_url
                }
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

