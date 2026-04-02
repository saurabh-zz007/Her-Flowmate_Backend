from pydantic import BaseModel, Date

class PregnancyCreateModel(BaseModel):
    conception_date:Date
    due_date:Date
    weeks_at_start:int

    