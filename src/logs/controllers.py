import uuid
from sqlalchemy.orm import Session
from src.logs.models import PeriodModel
from typing import List
from datetime import date
from src.logs.data_transfer_objects import PeriodSchema

def get_periods(db:Session, user_id: uuid.UUID):
    logs = db.query(PeriodModel).filter(PeriodModel.user_id == user_id).order_by(PeriodModel.start_date).all()
    return logs

def create_periods(data: PeriodSchema, db:Session, user_id: uuid.UUID):
    period = db.query(PeriodModel).filter(PeriodModel.user_id == user_id, PeriodModel.start_date == data.start_date).first()

    if period:
        raise Exception("Period log for this start date already exists")
    
    try:
        new_period = PeriodModel(
            user_id = user_id,
            start_date = data.start_date,
            end_date = data.end_date,
            duration = data.duration,
            flow_intensity = data.flow_intensity,
            mood = data.mood,
            symptoms = data.symptoms
        )
        db.add(new_period)
        db.commit()
        db.refresh(new_period)
        return new_period

    except Exception as e:
        db.rollback()
        raise e

def delete_periods(start_date: date, db: Session, user_id: uuid.UUID):
    period = db.query(PeriodModel).filter(PeriodModel.user_id == user_id, PeriodModel.start_date == start_date).first()

    if not period:
        raise Exception("Period log not found")
    
    try:
        period_data = period
        db.delete(period)
        db.commit()
        return period_data
    except Exception as e:
        db.rollback()
        raise e

def update_daily_log():
    pass

def get_daily_log():
    pass

def trends():
    pass