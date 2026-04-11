from pydantic import BaseModel
from datetime import date

class PeriodSchema(BaseModel):
    start_date: date
    end_date : date| None = None
    duration: int| None = None
    flow_intensity :str| None = None
    mood :str| None = None
    symptoms :list[str]| None = None

class DailyLogSchema(BaseModel):
    log_date: date
    moods: list[str]| None = None
    symptoms: list[str]| None = None
    water_intake: int = 0
    flow_intensity: str| None = None
    physical_activity : list[str] | None = None
    notes: str| None = None