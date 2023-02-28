from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean

class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True ,autoincrement=True)
    name = Column(String(120))
    status = Column(Boolean, default=True)