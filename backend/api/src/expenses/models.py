from models.get_db import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from category.models import Category

class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now)

    category = relationship("Category", back_populates = 'expenses')
