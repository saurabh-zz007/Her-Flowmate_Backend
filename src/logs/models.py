from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.utils.db import Base

class PeriodModel(Base):
    __tablename__ = "periods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    duration = Column(Integer)
    flow_intensity = Column(String(20))
    mood = Column(String(50))
    symptoms = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

