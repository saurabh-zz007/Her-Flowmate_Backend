import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.pregnancy import controllers
from src.pregnancy.data_transfer_objects import PregnancySchema
from src.utils.db import get_db
from src.utils.helpers import get_user_id

pregnancy_router = APIRouter(prefix="/pregnancy")

@pregnancy_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pregnancy(data: PregnancySchema, db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.create_pregnancy(data, user_id, db)

@pregnancy_router.get("/", status_code=status.HTTP_200_OK)
async def get_pregnancy(db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return await controllers.get_pregnancy(user_id, db)

