from pydantic import BaseModel, Field
from datetime import datetime


class CategoryDTO(BaseModel):
    id: int
    category_name:str

class CreateCategoryDTO(BaseModel):
    category_name:str =Field(max_length=1000)
