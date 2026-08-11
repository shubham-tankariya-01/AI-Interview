#external imports
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

#internals 
from core.database import get_db
from models.interview import InterviewSession
from schemas.interview import InterviewCreate, InterviewResponse

interview_router = APIRouter()

@interview_router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db)):
    try:
        db_interview_session = InterviewSession(user_name=interview.user_name, persona=interview.persona)
        db.add(db_interview_session)
        db.commit()
        db.refresh(db_interview_session)
        
        logger.info(f"Interview session created successfully for {interview.user_name}")
        return db_interview_session
        
    except SQLAlchemyError as db_err:
        db.rollback()
        logger.error(f"Database error during creation: {db_err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred."
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )