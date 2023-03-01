from app.models.base import BaseModel
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class OrderModel(BaseModel):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_price = Column(Float(precision=2))
    date_create = Column(Date, default=func.now())
    date_shipping = Column(Date)

    checkout_id = Column(String(255), nullable=True)
    checkout_url = Column(String(255), nullable=True)
    payment_status = Column(String(255), nullable=True)
    payment_detail = Column(String(255), nullable=True)

    status = Column(String, default='pending')

    items = relationship('OrderItemModel', uselist=True,
                         back_populates='order')
