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

@logs_router.post("/daily")
def update_daily_log():
    return controllers.update_daily_log()

@logs_router.get("/daily")
def get_daily_log():
    return controllers.get_daily_log()

@logs_router.get("/trends")
def get_trends():
    return controllers.trends()
