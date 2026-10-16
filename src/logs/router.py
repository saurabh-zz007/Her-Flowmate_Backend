import uuid
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.logs import controllers
from src.logs.data_transfer_objects import PeriodSchema, DailyLogSchema
from src.utils.db import get_db
from src.utils.helpers import get_user_id

logs_router = APIRouter(prefix="/logs")

@logs_router.get("/periods", response_model=List[PeriodSchema], status_code=status.HTTP_200_OK)
async def get_periods(db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.get_periods(db, user_id)

@logs_router.post("/periods", response_model=PeriodSchema, status_code=status.HTTP_201_CREATED)
async def create_periods(data: PeriodSchema, db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.create_periods(data, db, user_id)

@logs_router.delete("/periods", status_code=status.HTTP_204_NO_CONTENT)
async def delete_periods(start_date: date, db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.delete_periods(start_date, db, user_id)

@logs_router.post("/daily", response_model=DailyLogSchema, status_code=status.HTTP_201_CREATED)
async def update_daily_log(data: DailyLogSchema, db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.update_daily_log(data, db, user_id)

@logs_router.get("/daily", response_model=DailyLogSchema, status_code=status.HTTP_200_OK)
async def get_daily_log(log_date: date, db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.get_daily_log(log_date, db, user_id)

@logs_router.get("/trends", response_model=List[DailyLogSchema], status_code=status.HTTP_200_OK)
async def get_trends(range: int = 7, db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.trends(range, db, user_id)

