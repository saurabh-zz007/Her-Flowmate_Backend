from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from src.utils.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(100))
    photo_url = Column(String, nullable=True)
    age = Column(Integer)
    goal = Column(String(50), default='track_cycle')
    is_minimal_mode = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    on_update = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())

