from fastapi import APIRouter, Request, Depends, status
from src.auth.data_transfer_objects import authData
from src.auth.controllers import authentication
from src.utils.db import get_db

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/google", status_code=status.HTTP_200_OK)
def google_auth(request: Request, auth_data: authData, db = Depends(get_db)):
    return authentication(request, auth_data, db)

