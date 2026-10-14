import uuid
from sqlalchemy import select
from database.connection import SessionLocal
from models.message import Message

def get_message(message_id: str):
    db = SessionLocal()
    try:
        return db.execute(select(Message).where(Message.id == message_id)).scalar_one_or_none()
    finally:
        db.close()

def list_messages_by_conversation(conversation_id: str):
    db = SessionLocal()
    try:
        stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        return list(db.execute(stmt).scalars().all())
    finally:
        db.close()

def create_message(conversation_id: str, sender: str, content: str):
    db = SessionLocal()
    try:
        msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            sender=sender,
            content=content,
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg
    finally:
        db.close()
        
def delete_message(message_id: str):
    db = SessionLocal()
    try:
        msg = db.execute(select(Message).where(Message.id == message_id)).scalar_one_or_none()
        if msg is None:
            return None
        db.delete(msg)
        db.commit()
        return msg
    finally:
        db.close()


