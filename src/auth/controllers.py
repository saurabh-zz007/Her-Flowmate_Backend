from fastapi import Request, HTTPException
from google.oauth2 import id_token
import requests
from src.auth.data_transfer_objects import authData
from src.utils.settings import settings
from sqlalchemy.orm import Session
from src.user.models import UserModel
import jwt

def authentication(request: Request, auth_data: authData, db: Session):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user = id_token.verify_oauth2_token(auth_data.token, requests.Request(), settings.GOOGLE_CLOUD_CLIENT_ID)
        
        db_user = db.query(UserModel).filter(UserModel.email == user["email"]).first()

        if not db_user:
            try:
                db_user = UserModel(
                    email = user["email"],
                    display_name = user["name"],
                    photo_url = user["picture"],
                    #future data
                    age = None,
                    goal = "track_cycle",
                    is_minimal_mode = False
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)

                token = jwt.encode({"user_id": db_user.id}, settings.SECRET_KEY, settings.ALGORITHM) # type: ignore
                return token
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail="Error creating user: " + str(e))
        else:
            return {}

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid token: " + str(e))
