from sqlalchemy.orm import Session
import models

def get_chat_history(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve the most recent chat history entries.
    """
    return db.query(models.ChatHistory).order_by(models.ChatHistory.timestamp.desc()).offset(skip).limit(limit).all()

def create_chat_history(db: Session, user_message: str, bot_reply: str):
    """
    Create and save a new chat history entry.
    """
    db_chat_entry = models.ChatHistory(user_message=user_message, bot_reply=bot_reply)
    db.add(db_chat_entry)
    db.commit()
    db.refresh(db_chat_entry)
    return db_chat_entry
