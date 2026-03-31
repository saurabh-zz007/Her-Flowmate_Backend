from fastapi import APIRouter, Request, Depends
from src.auth.data_transfer_objects import authData
from src.auth.controllers import authentication
from src.utils.db import get_db

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/google")
def google_auth(request: Request, auth_data: authData, db = Depends(get_db)):
    print("hellow")
    return authentication(request, auth_data, db)

