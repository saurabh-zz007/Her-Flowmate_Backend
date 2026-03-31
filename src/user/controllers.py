from sqlalchemy.dialects.postgresql import UUID
from src.user.data_transfer_objects import UserUpdateSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException, Request
import uuid
from src.utils.helpers import get_user_id
from src.utils.settings import settings

def fetch_user(request:Request, db: Session):
    user_id = get_user_id(request.headers.get("Authorization", "").replace("jwt ", ""), settings.SECRET_KEY, settings.ALGORITHM)
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