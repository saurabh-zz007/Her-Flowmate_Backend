from fastapi import Request
from google.oauth2 import id_token
import requests
from src.auth.data_transfer_objects import authData
from src.utils.settings import settings
from sqlalchemy.orm import Session
from src.user.models import UserModel

def authentication(request: Request, auth_data: authData, db: Session):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user = id_token.verify_oauth2_token(auth_data.token, requests.Request(), settings.GOOGLE_CLOUD_CLIENT_ID)
        
        db_user = db.query(UserModel).filter(UserModel.email == user["email"]).first()

        if not db_user:
            try:
                db_user = UserModel(
                    id = user["sub"],
                    email = user["email"],
                    display_name = user["name"],
                    photo_url = user["picture"],
                    age = user.get("age"),
                    goal = user.get("goal", "track_cycle"),
                    is_minimal_mode = user.get("is_minimal_mode", False)
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
            except Exception as e:
                raise ValueError(f"Error creating user: {str(e)}")
        else:
            return {}

    except ValueError as e:
        return {
                "error": str(e),
        }
