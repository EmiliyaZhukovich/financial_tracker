from models.get_db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False)




class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now)

