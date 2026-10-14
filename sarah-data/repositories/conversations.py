import uuid
from sqlalchemy import select
from database.connection import SessionLocal
from models.conversation import Conversation


def get_conversation(conversation_id: str):
    db = SessionLocal()
    try:
        return db.execute(select(Conversation).where(Conversation.id == conversation_id)).scalar_one_or_none()
    finally:
        db.close()


def list_conversations(patient_id: str | None = None):
    db = SessionLocal()
    try:
        stmt = select(Conversation)
        if patient_id:
            stmt = stmt.where(Conversation.patient_id == patient_id)
        return list(db.execute(stmt).scalars().all())
    finally:
        db.close()


def create_conversation(patient_id: str):
    db = SessionLocal()
    try:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            patient_id=patient_id,
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    finally:
        db.close()


def delete_conversation(conversation_id: str):
    db = SessionLocal()
    try:
        conversation = db.execute(select(Conversation).where(Conversation.id == conversation_id)).scalar_one_or_none()
        if conversation is None:
            return None
        db.delete(conversation)
        db.commit()
        return conversation
    finally:
        db.close()