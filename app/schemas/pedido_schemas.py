from flask_restx import fields

class PedidoRequestSchema:
    def __init__(self, namespace):
        self.namespace = namespace
    
    def create(self):
        return self.namespace.model('Pedido Create',{
            'date_shipping':fields.Date(required=True)
        })