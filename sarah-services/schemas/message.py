from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel): # (define)   define la estructura para crear un mensaje, con los campos conversation_id, sender y content
    sender: str
    content: str


class MessageResponse(BaseModel): # (define)   define la estructura de respuesta de un mensaje, con los campos id, conversation_id, sender, content y created_at
    id: str
    conversation_id: str
    sender: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)