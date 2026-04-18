from fastapi import APIRouter, Depends, Request, status
from src.user import controllers
from sqlalchemy.dialects.postgresql import UUID
import uuid 
from src.utils.db import get_db
from src.user.data_transfer_objects import UserUpdateSchema, UserResponseSchema
from src.utils.helpers import get_user_id


user_route = APIRouter(prefix="/user")

@user_route.get("/profile", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def fetch_user(db = Depends(get_db), user_id:uuid.UUID = Depends(get_user_id)):
    return controllers.fetch_user(db, user_id)

@user_route.put("/profile", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def update_user( user_data: UserUpdateSchema,user_id: uuid.UUID = Depends(get_user_id), db = Depends(get_db)):
    return controllers.update_user(user_id, db, user_data)
