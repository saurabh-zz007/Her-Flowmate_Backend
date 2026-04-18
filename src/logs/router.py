from fastapi import APIRouter, Depends, status
from src.logs import controllers
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.helpers import get_user_id
import uuid
from src.logs.models import PeriodModel
from datetime import date
from src.logs.data_transfer_objects import PeriodSchema, DailyLogSchema

logs_router = APIRouter(prefix="/logs")

@logs_router.get("/periods", response_model=list[PeriodSchema], status_code=status.HTTP_200_OK)
def get_periods(db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.get_periods(db, user_id)

@logs_router.post("/periods", response_model=PeriodSchema, status_code=status.HTTP_201_CREATED)
def create_periods(data: PeriodSchema, db:Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.create_periods(data, db, user_id)

@logs_router.delete("/periods", response_model=PeriodSchema, status_code=status.HTTP_204_NO_CONTENT)
def delete_periods(start_date: date, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.delete_periods(start_date, db, user_id)

@logs_router.post("/daily", response_model=DailyLogSchema, status_code=status.HTTP_201_CREATED)
def update_daily_log(data: DailyLogSchema, db : Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.update_daily_log(data, db, user_id)

@logs_router.get("/daily", response_model=DailyLogSchema, status_code=status.HTTP_200_OK)
def get_daily_log(log_date : date, db : Session = Depends(get_db), user_id : uuid.UUID = Depends(get_user_id)):
    return controllers.get_daily_log(log_date, db, user_id)

@logs_router.get("/trends", response_model = list[DailyLogSchema], status_code=status.HTTP_200_OK)
def get_trends(range: int = 7, db: Session = Depends(get_db), user_id:uuid.UUID = Depends(get_user_id)):
    return controllers.trends(range, db, user_id)
