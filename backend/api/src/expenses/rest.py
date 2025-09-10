from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.get_db import get_db
from .models import Expenses
from .dto import ExpensesDTO, CreateExpensesDTO, UpdateExpensesDTO
from category.models import Category

router = APIRouter()


@router.get('/expenses', response_model=List[ExpensesDTO], status_code=200)
async def get_expenses(db:Session = Depends(get_db)):
    try:
        expenses = db.query(Expenses).all()
        return expenses
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail = f'Error {e}')

@router.post('/expenses', response_model=ExpensesDTO, status_code=201)
async def create_expense(data: CreateExpensesDTO, db: Session = Depends(get_db)):
    try:
        # Проверка существования категории
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category with this ID does not exist")

        # Создание нового объекта Expenses
        new = Expenses(
            category_id=data.category_id,
            amount=data.amount,
            date=data.date
        )
        db.add(new)
        db.commit()  # Сохраняем изменения
        db.refresh(new)  # Обновляем объект для получения актуальных данных (например, id)
        return new
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()  # Откатываем транзакцию в случае ошибки
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')

# TODO: ХОЧУ ВЫВЕСТИ ВМЕСТО ID КАТЕГОРИИ, ИМЯ КАТЕГОРИИ
@router.put('/expenses/{expense_id}', response_model=ExpensesDTO, status_code=200)
async def update_expense(expense_id: int, data: UpdateExpensesDTO, db: Session = Depends(get_db)):
    try:
        existing = db.query(Expenses).filter(Expenses.id == expense_id).first()
        if not existing:
            raise HTTPException(status_code=400, detail="Expens with this ID does not exist")

        if data.category_id is not None:
            category = db.query(Category).filter(Category.id == data.category_id).first()
            if not category:
                raise HTTPException(status_code=400, detail="Category with this ID does not exist")
            existing.category_id = data.category_id
        if data.amount is not None:
            existing.amount = data.amount
        if data.date is not None:
            existing.date = data.date

        db.commit()  # Сохраняем изменения
        db.refresh(existing)  # Обновляем объект для получения актуальных данных (например, id)
        return existing
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()  # Откатываем транзакцию в случае ошибки
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')


@router.delete('/expenses/{expense_id}', status_code=200)
async def update_expense(expense_id: int, db: Session = Depends(get_db)):
    try:
        existing = db.query(Expenses).filter(Expenses.id == expense_id).first()
        if not existing:
            raise HTTPException(status_code=400, detail="Expens with this ID does not exist")

        db.delete(existing)
        db.commit()  # Сохраняем изменения
        return "delete seccess"
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()  # Откатываем транзакцию в случае ошибки
        raise HTTPException(status_code=500, detail=f'Error: {str(e)}')
