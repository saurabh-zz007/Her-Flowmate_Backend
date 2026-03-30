from fastapi import APIRouter
from src.pregnancy import controllers

pregnancy_router = APIRouter(prefix="/pregnancy")

@pregnancy_router.post("/")
def create_pregnancy():
    return controllers.create_pregnancy()

@pregnancy_router.get("/")
def get_pregnancy():
    return controllers.get_pregnancy()
