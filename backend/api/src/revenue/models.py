from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from models.get_db import Base

class Revenue(Base):
    __tablename__ = 'revenues'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String(255), nullable=False)
