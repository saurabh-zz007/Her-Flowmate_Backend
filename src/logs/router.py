from fastapi import APIRouter, Depends
from src.logs import controllers
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.helpers import get_user_id
import uuid
from src.logs.models import PeriodModel
from datetime import date
from src.logs.data_transfer_objects import PeriodSchema

logs_router = APIRouter(prefix="/logs")

@logs_router.get("/periods", response_model=list[PeriodSchema])
def get_periods(db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.get_periods(db, user_id)

@logs_router.post("/periods", response_model=PeriodSchema)
def create_periods(data: PeriodSchema, db:Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.create_periods(data, db, user_id)

@logs_router.delete("/periods", response_model=PeriodSchema)
def delete_periods(start_date: date, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.delete_periods(start_date, db, user_id)

@logs_router.post("/daily")
def update_daily_log():
    return controllers.update_daily_log()

@logs_router.get("/daily")
def get_daily_log():
    return controllers.get_daily_log()

@logs_router.get("/trends")
def get_trends():
    return controllers.trends()
