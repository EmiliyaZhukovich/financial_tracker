from sqlalchemy.orm import Session
from datetime import datetime
from .models import Revenue
from .dto import RevenueCreateDTO, RevenueDTO

class RevenueService:
    @staticmethod
    def create_revenue(db: Session, revenue_data: RevenueCreateDTO) -> Revenue:
        """Создать новый доход"""
        # Если дата не указана, используем текущую дату
        if revenue_data.date is None:
            revenue_data.date = datetime.now()

        db_revenue = Revenue(
            amount=revenue_data.amount,
            description=revenue_data.description,
            date=revenue_data.date
        )

        db.add(db_revenue)
        db.commit()
        db.refresh(db_revenue)
        return db_revenue

    @staticmethod
    def get_revenues(db: Session, skip: int = 0, limit: int = 100) -> list[Revenue]:
        """Получить список доходов"""
        return db.query(Revenue).offset(skip).limit(limit).all()

    @staticmethod
    def get_revenue_by_id(db: Session, revenue_id: int) -> Revenue | None:
        """Получить доход по ID"""
        return db.query(Revenue).filter(Revenue.id == revenue_id).first()

    @staticmethod
    def update_revenue(db: Session, revenue_id: int, revenue_data: RevenueCreateDTO) -> Revenue | None:
        """Обновить доход"""
        db_revenue = db.query(Revenue).filter(Revenue.id == revenue_id).first()
        if not db_revenue:
            return None

        db_revenue.amount = revenue_data.amount
        db_revenue.description = revenue_data.description
        if revenue_data.date:
            db_revenue.date = revenue_data.date

        db.commit()
        db.refresh(db_revenue)
        return db_revenue

    @staticmethod
    def delete_revenue(db: Session, revenue_id: int) -> bool:
        """Удалить доход"""
        db_revenue = db.query(Revenue).filter(Revenue.id == revenue_id).first()
        if not db_revenue:
            return False

        db.delete(db_revenue)
        db.commit()
        return True

