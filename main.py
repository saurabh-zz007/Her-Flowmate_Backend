from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from google.oauth2 import id_token
from google.auth.transport import requests

app = FastAPI()
load_dotenv()



class authData(BaseModel):
    token: str


@app.post("/auth")
def authentication(request: Request, auth_data: authData):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user = id_token.verify_oauth2_token(auth_data.token, requests.Request(), os.getenv("GOOGLE_CLOUD_CLIENT_ID"))

        request.session['user'] = dict({
            "email" : user["email"] 
        })
        
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

@app.get('/')
def check(request:Request):
    return "hi "+ str(request.session.get('user')['email']) # type: ignore

