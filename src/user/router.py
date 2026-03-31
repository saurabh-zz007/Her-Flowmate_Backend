from fastapi import APIRouter, Depends, Request
from src.user import controllers
from sqlalchemy.dialects.postgresql import UUID
import uuid 
from src.utils.db import get_db
from src.user.data_transfer_objects import UserUpdateSchema

user_route = APIRouter(prefix="/user")

@user_route.get("/profile")
def fetch_user(request : Request, db = Depends(get_db)):
    return controllers.fetch_user(request, db)

@user_route.put("/profile")
def update_user(user_id: uuid.UUID, user_data: UserUpdateSchema, db = Depends(get_db)):
    print("Updating user:", user_id)
    return controllers.update_user(user_id, db, user_data)
