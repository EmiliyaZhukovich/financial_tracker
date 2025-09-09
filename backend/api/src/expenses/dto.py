from pydantic import BaseModel, Field
from datetime import datetime


class CategoryDTO(BaseModel):
    id: int
    category_name:str

class CreateCategoryDTO(BaseModel):
    category_name:str =Field(max_length=1000)

class ExpensesDTO(BaseModel):
    id: int
    category_id: int
    amount: int
    date: datetime

    class Config:
        from_attributes = True

