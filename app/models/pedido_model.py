from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class PedidoModel(BaseModel):
    __tablename__ = 'pedido'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_create = Column(Date, default=func.now())
    date_shipping = Column(Date)
    total_price = Column(Float(precision=2))

    payment_status = Column(String(255), nullable=True)
    payment_detail = Column(String(255), nullable=True)

    status = Column(String, default='pending')

    # Relacion al usuario
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relacion a pedido_items
    items = relationship('PedidoItemModel', uselist=True, back_populates='pedido')
