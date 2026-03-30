from fastapi import APIRouter
from src.logs import controllers


logs_router = APIRouter(prefix="/logs")

@logs_router.get("/periods")
def get_periods():
    return controllers.get_periods()

@logs_router.post("/periods")
def create_periods():
    return controllers.create_periods()

@logs_router.delete("/periods")
def delete_periods():
    return controllers.delete_periods()



