from models.get_db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False)

    expenses = relationship("Expenses", back_populates="category")
