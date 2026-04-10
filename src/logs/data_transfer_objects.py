from pydantic import BaseModel
from datetime import date

class PeriodSchema(BaseModel):
    start_date: date
    end_date : date| None = None
    duration: int| None = None
    flow_intensity :str| None = None
    mood :str| None = None
    symptoms :list[str]| None = None