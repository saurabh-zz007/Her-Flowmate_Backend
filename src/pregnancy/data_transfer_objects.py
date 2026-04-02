from pydantic import BaseModel, Field
from datetime import date

class PregnancySchema(BaseModel):
    conception_date:date|None = None
    due_date:date|None = None
    weeks_at_start:int|None = None


    

