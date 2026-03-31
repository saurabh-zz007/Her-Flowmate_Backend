from fastapi import Request
from google.oauth2 import id_token
import requests
from src.auth.data_transfer_objects import authData
from src.utils.settings import settings

def authentication(request: Request, auth_data: authData):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user = id_token.verify_oauth2_token(auth_data.token, requests.Request(), settings.GOOGLE_CLOUD_CLIENT_ID)
        
        return {
            "email": user["email"],
            "email_verified": user["email_verified"],
            "name": user["name"],
            "picture": user["picture"],
            "given_name": user["given_name"],
            "family_name": user["family_name"],
        }

    except ValueError as e:
        return {
                "error": str(e),
        }
