from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RevenueCreateDTO(BaseModel):
    amount: int = Field(gt=0, description="Сумма дохода должна быть больше 0")
    description: str = Field(min_length=1, max_length=255, description="Описание дохода")
    date: Optional[datetime] = Field(default=None, description="Дата дохода (по умолчанию текущая дата)")

class RevenueUpdateDTO(BaseModel):
    amount: Optional[int] = Field(None, gt=0, description="Сумма дохода должна быть больше 0")
    description: Optional[str] = Field(None, min_length=1, max_length=255, description="Описание дохода")
    date: Optional[datetime] = Field(None, description="Дата дохода")

class RevenueDTO(BaseModel):
    id: int
    amount: int
    description: str
    date: datetime

    class Config:
        from_attributes = True

