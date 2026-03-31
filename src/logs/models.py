from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, ARRAY, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.utils.db import Base

class PeriodModel(Base):
    __tablename__ = "period_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    duration = Column(Integer)
    flow_intensity = Column(String(20))
    mood = Column(String(50))
    symptoms = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DailyLogModel(Base):
    __tablename__ = "daily_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    log_date = Column(Date, nullable=False)
    moods = Column(ARRAY(String))
    symptoms = Column(ARRAY(String))
    water_intake = Column(Integer, default=0)
    flow_intensity = Column(String(20))
    physical_activity = Column(ARRAY(String))
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'log_date', name='unique_daily_log_per_user'),
    )