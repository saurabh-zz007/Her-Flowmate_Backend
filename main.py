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
from src.pregnancy.router import pregnancy_router
from src.logs.router import logs_router

Base.metadata.create_all(engine)

app = FastAPI(title="Her-Flowmate")
app.include_router(user_route)
app.include_router(pregnancy_router)
app.include_router(logs_router)






