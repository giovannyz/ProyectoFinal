from flask_restx import fields


class PedidoRequestSchema:
    def __init__(self, namespace):
        self.namespace = namespace

    def create(self):
        return self.namespace.model('Pedido Create', {
            'coupon': fields.String(required=False, max_length=50),
            'date_shipping': fields.Date(required=True)
        })
