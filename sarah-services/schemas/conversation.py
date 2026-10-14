from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel): # (define)   define la estructura para crear una conversación, con los campos patient_id y professional_id
    patient_id: str
    professional_id: str | None = None


class ConversationResponse(BaseModel): # (define)   define la estructura de respuesta de una conversación, con los campos id, patient_id, professional_id, created_at, start_time y end_time
    id: str
    patient_id: str
    professional_id: str | None = None
    created_at: datetime
    start_time: datetime
    end_time: datetime | None = None

    model_config = ConfigDict(from_attributes=True)