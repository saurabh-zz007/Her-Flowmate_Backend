from src import user
from src.pregnancy.data_transfer_objects import PregnancySchema
from src.pregnancy.models import PregnancyModel
from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException

def create_pregnancy(data: PregnancySchema, user_id: uuid.UUID, db: Session):
    try:
        pregnancy_data = db.query(PregnancyModel).filter(PregnancyModel.user_id == user_id).first()
        #if pregnancy model dont exists => Create it
        if not pregnancy_data:
            pregnancy_data = PregnancyModel(user_id=user_id, conception_date=data.conception_date, due_date=data.due_date, weeks_at_start=data.weeks_at_start)
            db.add(pregnancy_data)
        else:
            #if it exists => Update it
            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(pregnancy_data, key, value)
        db.commit()
        db.refresh(pregnancy_data)
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating pregnancy: " + str(e))
    return pregnancy_data

def get_pregnancy(user_id: uuid.UUID, db: Session):
    try:
        pregnancy_data = db.query(PregnancyModel).filter(PregnancyModel.user_id == user_id).first()
        if not pregnancy_data:
            raise HTTPException(status_code=404, detail="Pregnancy data not found")
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="Error fetching pregnancy data: " + str(e))
    return pregnancy_data