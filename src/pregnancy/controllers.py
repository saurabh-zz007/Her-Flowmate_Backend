import uuid
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.pregnancy.data_transfer_objects import PregnancySchema
from src.pregnancy.models import PregnancyModel

async def create_pregnancy(data: PregnancySchema, user_id: uuid.UUID, db: AsyncSession):
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
        return pregnancy_data
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating pregnancy: {str(e)}")

async def get_pregnancy(user_id: uuid.UUID, db: AsyncSession):
    stmt = select(PregnancyModel).where(PregnancyModel.user_id == user_id)
    result = await db.execute(stmt)
    pregnancy_data = result.scalars().first()
    if not pregnancy_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregnancy data not found")
    return pregnancy_data