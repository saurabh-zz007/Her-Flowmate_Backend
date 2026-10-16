import uuid
from datetime import date, timedelta
from typing import List
from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.logs.data_transfer_objects import PeriodSchema, DailyLogSchema
from src.logs.models import PeriodModel, DailyLogModel

async def get_periods(db: AsyncSession, user_id: uuid.UUID) -> List[PeriodModel]:
    stmt = select(PeriodModel).where(PeriodModel.user_id == user_id).order_by(PeriodModel.start_date)
    result = await db.execute(stmt)
    logs = list(result.scalars().all())
    if not logs:
        raise HTTPException(status_code=404, detail="No periods found")
    return logs

async def create_periods(data: PeriodSchema, db: AsyncSession, user_id: uuid.UUID) -> PeriodModel:
    stmt = select(PeriodModel).where(PeriodModel.user_id == user_id, PeriodModel.start_date == data.start_date)
    result = await db.execute(stmt)
    period = result.scalars().first()

    if period:
        raise HTTPException(status_code=400, detail="Period log for this start date already exists")

    try:
        new_period = PeriodModel(
            user_id=user_id,
            start_date=data.start_date,
            end_date=data.end_date,
            duration=data.duration,
            flow_intensity=data.flow_intensity,
            mood=data.mood,
            symptoms=data.symptoms
        )
        db.add(new_period)
        await db.commit()
        return new_period

    except Exception as e:
        await db.rollback()
        raise e

async def delete_periods(start_date: date, db: AsyncSession, user_id: uuid.UUID):
    stmt = (
        delete(PeriodModel)
        .where(PeriodModel.user_id == user_id, PeriodModel.start_date == start_date)
        .returning(PeriodModel.id)
    )
    try:
        result = await db.execute(stmt)
        deleted_id = result.scalars().first()
        if not deleted_id:
            raise HTTPException(status_code=404, detail="Period log not found")
        await db.commit()
        return None
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise e

async def update_daily_log(data: DailyLogSchema, db: AsyncSession, user_id: uuid.UUID) -> DailyLogModel:
    payload = data.model_dump(exclude_unset=True)
    update_dict = {k: v for k, v in payload.items() if k != "log_date"}
    if not update_dict:
        update_dict = {"notes": payload.get("notes")}

    stmt = (
        pg_insert(DailyLogModel)
        .values(user_id=user_id, **payload)
        .on_conflict_do_update(
            index_elements=[DailyLogModel.user_id, DailyLogModel.log_date],
            set_=update_dict
        )
        .returning(DailyLogModel)
    )

    try:
        result = await db.execute(stmt)
        log = result.scalars().one()
        await db.commit()
        return log
    except Exception as e:
        await db.rollback()
        raise e

async def get_daily_log(log_date: date, db: AsyncSession, user_id: uuid.UUID) -> DailyLogModel:
    stmt = select(DailyLogModel).where(DailyLogModel.user_id == user_id, DailyLogModel.log_date == log_date)
    result = await db.execute(stmt)
    log = result.scalars().first()
    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found")
    return log

async def trends(range: int, db: AsyncSession, user_id: uuid.UUID) -> List[DailyLogModel]:
    end_date = date.today()
    start_date = end_date - timedelta(days=range)

    stmt = select(DailyLogModel).where(
        DailyLogModel.user_id == user_id,
        DailyLogModel.log_date >= start_date,
        DailyLogModel.log_date <= end_date
    ).order_by(DailyLogModel.log_date)
    result = await db.execute(stmt)
    logs = list(result.scalars().all())

    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for the specified range")
    
    return logs
