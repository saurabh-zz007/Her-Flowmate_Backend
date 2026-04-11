import uuid
from sqlalchemy import Column
from sqlalchemy.orm import Session
from src.logs.models import PeriodModel, DailyLogModel
from typing import List
from datetime import date, timedelta
from src.logs.data_transfer_objects import PeriodSchema, DailyLogSchema

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

def update_daily_log(data: DailyLogSchema, db: Session, user_id: uuid.UUID):
    log = db.query(DailyLogModel).filter(DailyLogModel.user_id == user_id, DailyLogModel.log_date == data.log_date).first()

    if not log:
        log = DailyLogModel(
            user_id = user_id,
            log_date = data.log_date,
            moods = data.moods,
            symptoms = data.symptoms,
            water_intake = data.water_intake,
            flow_intensity = data.flow_intensity,
            physical_activity = data.physical_activity,
            notes = data.notes
        )
    
    else:
        for field, value in data.model_dump().items():
            if value is not None:
                setattr(log, field, value)

    db.add(log)
    db.commit()
    db.refresh(log)

    return log

def get_daily_log(log_date: date, db:Session, user_id: uuid.UUID):
    log = db.query(DailyLogModel).filter(DailyLogModel.user_id == user_id, DailyLogModel.log_date == log_date).first()
    if not log:
        raise Exception("Daily log not found")
    return log

def trends(range : int, db: Session, user_id: uuid.UUID):
    end_date = date.today()
    start_date = end_date - timedelta(days=range)

    logs = db.query(DailyLogModel).filter(DailyLogModel.user_id == user_id, DailyLogModel.log_date >= start_date, DailyLogModel.log_date <= end_date).all()

    if not logs:
        raise Exception("No logs found for the specified range")
    
    return logs