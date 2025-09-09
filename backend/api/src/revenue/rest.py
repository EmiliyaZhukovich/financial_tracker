import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from models.get_db import get_db
from .models import Revenue
from .dto import RevenueDTO, RevenueCreateDTO, RevenueUpdateDTO

router = APIRouter()

@router.get("/revenues", response_model=List[RevenueDTO])
async def get_revenue(db: Session = Depends(get_db)):
    try:
        my_revenue = db.query(Revenue).all()
        return my_revenue
    except Exception as e:
        raise HTTPException(status_code=404, detail='Not found revenues')

@router.get("/revenues/{revenue_id}", response_model=RevenueDTO)
async def get_revenue_id(revenue_id: int, db: Session = Depends(get_db)):
    try:
        my_revenue = db.query(Revenue).filter(Revenue.id == revenue_id).first()
        if not my_revenue:
            raise HTTPException(status_code=404, detail='Revenue not found')
        return my_revenue
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error getting revenue: {str(e)}')


@router.post("/revenues", response_model=RevenueDTO, status_code=201)
async def create_revenue(revenue_data: RevenueCreateDTO, db: Session = Depends(get_db)):
    try:
        new_revenue = Revenue(
            amount = revenue_data.amount,
            description=revenue_data.description,
            date = revenue_data.date if revenue_data.date else datetime.datetime.now()
        )
        db.add(new_revenue)
        db.commit()
        db.refresh(new_revenue)
        return new_revenue
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f'Error creating revenue: {str(e)}')

@router.put("/revenues/{revenue_id}", response_model=RevenueDTO, status_code=200)
async def update_revenue(revenue_id: int, revenue_data: RevenueUpdateDTO, db: Session = Depends(get_db)):
    try:
        existing_revenue = db.query(Revenue).filter(Revenue.id == revenue_id).first()
        print(existing_revenue)
        if not existing_revenue:
            raise HTTPException(status_code=404, detail='I cant find revenue')

        # Обновляем только те поля, которые переданы (не None)
        if revenue_data.amount is not None:
            existing_revenue.amount = revenue_data.amount
        if revenue_data.description is not None:
            existing_revenue.description = revenue_data.description
        if revenue_data.date is not None:
            existing_revenue.date = revenue_data.date

        db.commit()
        db.refresh(existing_revenue)
        return existing_revenue
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error in update_revenue: {str(e)}")
        raise HTTPException(status_code=400, detail=f'Error updating revenue: {str(e)}')

@router.delete("/revenues/{revenue_id}", status_code=200)
async def delete_revenue(revenue_id: int, db: Session = Depends(get_db)):
    try:
        existing_revenue = db.query(Revenue).filter(Revenue.id == revenue_id).first()
        if not existing_revenue:
            raise HTTPException(status_code=404, detail='I cant find revenue')

        db.delete(existing_revenue)
        db.commit()
        return {"message": "success delete revenue"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"Error in delete_revenue: {str(e)}")
        raise HTTPException(status_code=400, detail=f'Error deleting revenue: {str(e)}')
