from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExpensesDTO(BaseModel):
    id: int
    category_id:int
    amount: int
    date: datetime

    class Config:
        from_attributes = True


class CreateExpensesDTO(BaseModel):
    category_id: int
    amount: int = Field(ge=0)
    date: datetime = Field(default=datetime.now())

class UpdateExpensesDTO(BaseModel):
    category_id: Optional[int]
    amount: Optional[int] = Field(default=None, ge=0)
    date: Optional[datetime] = Field(default_factory=datetime.now)
