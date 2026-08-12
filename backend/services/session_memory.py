import logging
from sqlalchemy.orm import Session 
from models.transcript import Transcript

logger = logging.getLogger(__name__)

def save_transcript(db: Session, session_id: str, role: str, text: str) -> Transcript | None:
    """
    1. Create a new Transcript object with the provided data.
    2. Add it to the database, commit, and refresh.
    3. Return the saved transcript.
    """
    try:
        new_transcript = Transcript(
            session_id=session_id, 
            role=role, 
            text=text
        )
        db.add(new_transcript)
        db.commit()
        db.refresh(new_transcript)
        return new_transcript
    except Exception as e:
        logger.error(f"Error occurred while saving transcript: {e}")
        db.rollback()  # Important to rollback the transaction on error
        return None

def get_conversation_history(db: Session, session_id: str, limit: int = 15) -> str:
    """
    Order of the execution.....
    1.Query the Transcript table for this session_id, in query we let have all by desc() order
    2.so , Order the results by created_at ascending (oldest first).
    3. Limit the results to the last `limit` messages (so we don't blow up the LLM context window).
    4.Format the result into a single string.
    Example return string: 
    "user: Hello\nai: Hi there\nuser: How are you?"
    """
    try:
        #want the *last* `limit` messages, but we want them ordered *oldest first*.
        # Best way is to query ordered by desc, limit it, then reverse in Python.
        transcripts = (
            db.query(Transcript)
            .filter(Transcript.session_id == session_id)
            .order_by(Transcript.created_at.desc())
            .limit(limit)
            .all()
        )
        
        # Reverse the list in-place so it is chronological (oldest->newest)
        transcripts.reverse()
        
        history_lines = []
        for t in transcripts:
            history_lines.append(f"{t.role}: {t.text}")
            
        return "\n".join(history_lines)
        
    except Exception as e:
        logger.error(f"Error occurred while fetching conversation history: {e}")
        return ""