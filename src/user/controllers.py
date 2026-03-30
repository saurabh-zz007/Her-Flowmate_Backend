from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.user.data_transfer_objects import UserUpdateSchema
from src.utils.db import local_session
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException
import uuid

def fetch_user(user_id: uuid.UUID, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_name": user.display_name,
        "user_email": user.email,
        "user_age": user.age,
        "user_goal": user.goal
    }

def update_user(user_id: uuid.UUID, db: Session, user_data: UserUpdateSchema):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.model_dump().items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)

    return user