from fastapi import APIRouter, Depends, status
from src.pregnancy import controllers
from src.pregnancy.data_transfer_objects import PregnancySchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.helpers import get_user_id
import uuid

pregnancy_router = APIRouter(prefix="/pregnancy")

@pregnancy_router.post("/", status_code=status.HTTP_201_CREATED)
def create_pregnancy(data: PregnancySchema, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.create_pregnancy(data, user_id, db)

@pregnancy_router.get("/", status_code=status.HTTP_200_OK)
def get_pregnancy(db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_user_id)):
    return controllers.get_pregnancy(user_id, db)
