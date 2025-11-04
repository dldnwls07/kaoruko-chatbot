from sqlalchemy.orm import Session
import models

def get_chat_history(db: Session, user_name: str = None, skip: int = 0, limit: int = 10):
    """
    Retrieve the most recent chat history entries for a specific user.
    """
    query = db.query(models.ChatHistory)
    if user_name:
        query = query.filter(models.ChatHistory.user_name == user_name)
    return query.order_by(models.ChatHistory.timestamp.desc()).offset(skip).limit(limit).all()

def create_chat_history(db: Session, user_message: str, bot_reply: str, user_name: str = "사용자"):
    """
    Create and save a new chat history entry.
    """
    db_chat_entry = models.ChatHistory(user_message=user_message, bot_reply=bot_reply, user_name=user_name)
    db.add(db_chat_entry)
    db.commit()
    db.refresh(db_chat_entry)
    return db_chat_entry

def clear_user_data(db: Session, user_name: str):
    """
    Clear all data for a specific user (chat history, emotions, affection).
    """
    # ChatHistory 삭제
    db.query(models.ChatHistory).filter(models.ChatHistory.user_name == user_name).delete()
    
    # UserEmotion 삭제
    db.query(models.UserEmotion).filter(models.UserEmotion.user_name == user_name).delete()
    
    # UserAffection 삭제  
    db.query(models.UserAffection).filter(models.UserAffection.user_name == user_name).delete()
    
    # EmotionHistory 삭제
    db.query(models.EmotionHistory).filter(models.EmotionHistory.user_name == user_name).delete()
    
    db.commit()
    return True
