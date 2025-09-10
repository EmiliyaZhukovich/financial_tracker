from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.get_db import get_db
from .models import Category
from .dto import CategoryDTO, CreateCategoryDTO

router = APIRouter()


@router.get('/categories', response_model=List[CategoryDTO])
async def get_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Category).all()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error getting categories: {str(e)}')


@router.post('/categories', response_model=CategoryDTO, status_code=201)
async def create_category(new_data: CreateCategoryDTO, db: Session = Depends(get_db)):
    try:
        # Проверяем, существует ли уже категория с таким именем
        existing_category = db.query(Category).filter(Category.category_name == new_data.category_name).first()
        if existing_category:
            raise HTTPException(status_code=400, detail='Уже есть такое имя категории')

        # Создаем новую категорию
        new_category = Category(category_name=new_data.category_name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error creating category: {str(e)}')

@router.get('/categories/{category_name}', response_model=List[CategoryDTO])
async def get_categories(category_name: str, db: Session = Depends(get_db)):
    try:
        existing_category = db.query(Category).filter(Category.category_name==category_name)
        if not existing_category:
            raise HTTPException(status_code=404, detail='Нет такого имя категории')
        return existing_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error getting categories: {str(e)}')


@router.put('/categories/{category_id}', response_model=CategoryDTO, status_code=200)
async def update_category(category_id: int, new_data: CreateCategoryDTO, db: Session = Depends(get_db)):
    try:
        existing_category = db.query(Category).filter(Category.id==category_id).first()
        if not existing_category:
            raise HTTPException(status_code=404, detail='Нет такого имя категории')

        dublicate_category = db.query(Category).filter(
            Category.category_name == new_data.category_name,
            Category.id != category_id
        ).first() or db.query(Category).filter(
            Category.category_name == new_data.category_name,
            Category.id == category_id
        ).first()
        if dublicate_category:
            raise HTTPException(status_code=400, detail='Категория с таким именем уже существует')

        existing_category.category_name = new_data.category_name
        db.commit()
        db.refresh(existing_category)
        return existing_category
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error creating category: {str(e)}')

@router.delete('/categories/{category_id}', status_code=200)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        existing_category = db.query(Category).filter(Category.id==category_id).first()
        if not existing_category:
            raise HTTPException(status_code=404, detail='Нет такого имя категории')

        db.delete(existing_category)
        db.commit()
        return "success delete"
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Error delete category: {str(e)}')
