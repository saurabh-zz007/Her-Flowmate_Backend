from src.pregnancy.data_transfer_objects import PregnancyCreateModel
from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException

def create_pregnancy(data: PregnancyCreateModel, user_id: uuid.UUID, db: Session):
    try:
        pregnancy_data = db.query(PregnancyCreateModel).filter_by(user_id = user_id).first()
        #if pregnancy model dont exists => Create it
        if not pregnancy_data:
            pregnancy_data = PregnancyCreateModel(conception_date=data.conception_date, due_date=data.due_date, weeks_at_start=data.weeks_at_start)
            db.add(pregnancy_data)
            db.commit()
            db.refresh(pregnancy_data)
        else:
            #if it exists => Update it
            pregnancy_data.conception_date = data.conception_date
            pregnancy_data.due_date = data.due_date
            pregnancy_data.weeks_at_start = data.weeks_at_start
            db.commit()
            db.refresh(pregnancy_data)
    except HTTPException as e:
        db.rollback()
        raise e
    return pregnancy_data
    
def get_pregnancy():
    pass