from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class CategoryModel(BaseModel):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80))
    detalle = Column(String(160))
    status = Column(Boolean, default=True)

    products = relationship('ProductsModel', uselist=True, back_populates='category')
