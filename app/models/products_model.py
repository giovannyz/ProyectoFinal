from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class ProductsModel(BaseModel):
    __tablename__ = "products"
    # Componentes de nuestra tabla
    id = Column(Integer, primary_key=True, autoincrement=True)
    name =Column(String(120))
    description = Column(String(250))
    precio = Column(Integer)
    fecha = Column(Date, default=func.now())
    stock = Column(Integer)
    status = Column(Boolean, default=True)
    

    # Relacion al modelo Category
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('CategoryModel', uselist=False, back_populates='products')
    
    # Añadir un modelo que relacione la categoria independiente
    pedido_items = relationship('PedidoItemModel', uselist=True, back_populates='product')