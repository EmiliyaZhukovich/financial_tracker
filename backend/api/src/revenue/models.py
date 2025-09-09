from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from ..models.get_db import Base

class Revenue(Base):
    __tablename__ = 'revenues'

    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now)
    description = Column(String(255), nullable=False)
