from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
import uuid
from .base import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_name = Column(String, index=True)
    persona = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
