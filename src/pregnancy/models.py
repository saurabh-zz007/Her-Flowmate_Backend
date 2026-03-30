from sqlalchemy import Integer, DateTime, func, String, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.utils.db import Base

class PregnancyModel(Base):
    __tablename__ = "pregnancies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"), primary_key=True, unique=True)
    conception_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    weeks_at_start = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

