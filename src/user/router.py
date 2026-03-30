from fastapi import APIRouter, Depends
from src.user import controllers
from sqlalchemy.dialects.postgresql import UUID
import uuid 
from src.utils.db import get_db
from src.user.data_transfer_objects import UserUpdateSchema

user_route = APIRouter(prefix="/user")

@user_route.get("/profile")
def fetch_user(user_id: uuid.UUID, db = Depends(get_db)):
    return controllers.fetch_user(user_id, db)

@user_route.put("/profile")
def update_user(user_id: uuid.UUID, user_data: UserUpdateSchema, db = Depends(get_db)):
    return controllers.update_user(user_id, db, user_data)
