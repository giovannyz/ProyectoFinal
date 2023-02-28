from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Date, Boolean

class HolidayModel(BaseModel):
    __tablename__ = 'holidays'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    description = Column(String(120))
    status = Column(Boolean, default=True)