from app.models.base import BaseModel
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class PedidoItemModel(BaseModel):
    __tablename__ = 'pedido_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey('pedido.id'))
    pedido = relationship('PedidoModel', uselist=False, back_populates='items')

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('ProductsModel', uselist=False,
                           back_populates='pedido_items')
    
    price = Column(Float(precision=2))
    quantity = Column(Integer)
