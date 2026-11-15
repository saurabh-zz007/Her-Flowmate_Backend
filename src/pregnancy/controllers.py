import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.pregnancy.data_transfer_objects import PregnancySchema
from src.pregnancy.models import PregnancyModel

from src.utils.cache_service import CacheService


async def create_pregnancy(data: PregnancySchema, user_id: uuid.UUID, db: AsyncSession, cache: CacheService):
    cache_key = f"pregnancy:{user_id}"
    payload = data.model_dump(exclude_unset=True)
    stmt = (
        pg_insert(PregnancyModel)
        .values(user_id=user_id, **payload)
        .on_conflict_do_update(
            index_elements=[PregnancyModel.user_id],
            set_=payload
        )
        .returning(PregnancyModel)
    )
    try:
        result = await db.execute(stmt)
        pregnancy_data = result.scalars().one()
        await db.commit()
        await cache.delete(cache_key)
        return pregnancy_data
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating pregnancy: {str(e)}")

async def get_pregnancy(user_id: uuid.UUID, db: AsyncSession, cache: CacheService):
    cache_key = f"pregnancy:{user_id}"
    cached_data = await cache.get(cache_key)
    if cached_data:
        print("Returning cached pregnancy data")
        return cached_data
    stmt = select(PregnancyModel).where(PregnancyModel.user_id == user_id)
    result = await db.execute(stmt)
    pregnancy_data = result.scalars().first()
    if not pregnancy_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregnancy data not found")
    print("Caching pregnancy data")
    await cache.set(cache_key, pregnancy_data)
    print("Returning pregnancy data from database")
    return pregnancy_data
