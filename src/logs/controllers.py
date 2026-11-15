import uuid
from datetime import date, timedelta
from typing import List, Dict, Any, Union
from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.logs.data_transfer_objects import PeriodSchema, DailyLogSchema
from src.logs.models import PeriodModel, DailyLogModel
from src.utils.cache_service import CacheService

async def get_periods(db: AsyncSession, user_id: uuid.UUID, cache: CacheService) -> List[PeriodModel]:
    cache_key = f"periods:list:{user_id}"
    cached_data = await cache.get(cache_key)
    if cached_data:
        return cached_data
    stmt = select(PeriodModel).where(PeriodModel.user_id == user_id).order_by(PeriodModel.start_date)
    result = await db.execute(stmt)
    logs = list(result.scalars().all())
    if not logs:
        raise HTTPException(status_code=404, detail="No periods found")
    await cache.set(cache_key, logs)
    return logs

async def create_periods(data: PeriodSchema, db: AsyncSession, user_id: uuid.UUID, cache: CacheService) -> PeriodModel:
    cache_key = f"periods:list:{user_id}"
    await cache.delete(cache_key)
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

async def delete_periods(start_date: date, db: AsyncSession, user_id: uuid.UUID, cache: CacheService):
    cache_key = f"periods:list:{user_id}"
    await cache.delete(cache_key)
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

async def update_daily_log(data: DailyLogSchema, db: AsyncSession, user_id: uuid.UUID, cache: CacheService) -> DailyLogModel:
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
        await cache.delete(f"log:detail:{user_id}{log.log_date}")
        await cache.delete(f"log:list:{user_id}")
        return log
    except Exception as e:
        await db.rollback()
        raise e

async def get_daily_log(log_date: date, db: AsyncSession, user_id: uuid.UUID, cache: CacheService) -> DailyLogModel:
    cache_key = f"log:detail:{user_id}{log_date}"
    cached_data = await cache.get(cache_key)
    if cached_data:
        return cached_data
    stmt = select(DailyLogModel).where(DailyLogModel.user_id == user_id, DailyLogModel.log_date == log_date)
    result = await db.execute(stmt)
    log = result.scalars().first()
    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found")
    await cache.set(cache_key, log)
    return log

async def trends(range: int, db: AsyncSession, user_id: uuid.UUID, cache: CacheService) -> List[Union[DailyLogModel, Dict[str, Any]]]:
    end_date = date.today()
    start_date = end_date - timedelta(days=range)

    cache_key = f"log:list:{user_id}"
    all_logs = await cache.get(cache_key)

    if not all_logs:
        stmt = select(DailyLogModel).where(
            DailyLogModel.user_id == user_id,
        ).order_by(DailyLogModel.log_date.desc())
        result = await db.execute(stmt)
        all_logs = list(result.scalars().all())

        if not all_logs:
            raise HTTPException(status_code=404, detail="No logs found for the specified range")
        await cache.set(cache_key, all_logs)

    start_str = start_date.isoformat()
    end_str = end_date.isoformat()
    filtered_logs = []
    for log in all_logs:
        if isinstance(log, dict):
            log_date_str = str(log["log_date"])
        else:
            log_date_str = log.log_date.isoformat()

        if start_str <= log_date_str <= end_str:
            filtered_logs.append(log)
    return filtered_logs

