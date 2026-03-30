from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from src.utils.db import Base, engine
from src.utils.settings import settings
from pydantic import BaseModel
from src.user.router import user_route

Base.metadata.create_all(engine)

app = FastAPI(title="Her-Flowmate")
app.include_router(user_route)


class authData(BaseModel):
    token: str

@app.post("/auth")
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


