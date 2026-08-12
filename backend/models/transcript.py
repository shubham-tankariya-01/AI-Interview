from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        String, 
        ForeignKey("interview_sessions.session_id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    role = Column(String(50), nullable=False)  # e.g., 'user' or 'ai'
    text = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        index=True
    )

    # Relationship to the InterviewSession model
    session = relationship("InterviewSession", backref="transcripts")
