from fastapi import APIRouter, Request
from src.auth.data_transfer_objects import authData
from src.auth.controllers import authentication

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/google")
def google_auth(request: Request, auth_data: authData):
    return authentication(request, auth_data)

