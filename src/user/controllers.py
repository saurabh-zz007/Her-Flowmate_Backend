import uuid
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.user.data_transfer_objects import UserUpdateSchema
from src.user.models import UserModel

async def fetch_user(db: AsyncSession, user_id: uuid.UUID):
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def update_user(user_id: uuid.UUID, db: AsyncSession, user_data: UserUpdateSchema):
    payload = user_data.model_dump(exclude_unset=True)
    if not payload:
        return await fetch_user(db, user_id)

    stmt = (
        update(UserModel)
        .where(UserModel.id == user_id)
        .values(**payload)
        .returning(UserModel)
    )
    try:
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await db.commit()
        return user
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")
