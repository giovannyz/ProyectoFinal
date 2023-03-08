from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class ProductsModel(BaseModel):
    __tablename__ = "products"
    # Componentes de nuestra tabla
    id = Column(Integer, primary_key=True, autoincrement=True)
    name =Column(String(120))
    description = Column(String(250))
    precio = Column(Float(precision=2))
    fecha = Column(Date, default=func.now())
    stock = Column(Integer)
    status = Column(Boolean, default=True)
    

    # Relacion al modelo Category
    cat_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('CategoryModel', uselist=False, back_populates='products')
    
    # Relacion al modelo Shopping_cart
    shopping_carts = relationship('ShoppingCartModel', uselist=True, back_populates='product')

    # Añadir un modelo que relacione la categoria independiente
    pedido_items = relationship('PedidoItemModel', uselist=True, back_populates='product')