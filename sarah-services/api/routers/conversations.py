from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from repositories import conversations as convo_repo
from repositories import messages as msg_repo
from schemas.conversation import ConversationCreate, ConversationResponse
from schemas.message import MessageCreate, MessageResponse
from services.assistant import generate_sarah_response

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(data: ConversationCreate):
    try:
        return convo_repo.create_conversation(
            patient_id=data.patient_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en BD/Repo conversación: {str(e)}"
        )


@router.get("/", response_model=list[ConversationResponse])
def list_conversations(patient_id: str | None = None):
    return convo_repo.list_conversations(patient_id=patient_id)


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: str):
    convo = convo_repo.get_conversation(conversation_id)
    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversación con id '{conversation_id}' no encontrada",
        )
    return convo


@router.delete("/{conversation_id}", response_model=ConversationResponse)
def delete_conversation(conversation_id: str):
    convo = convo_repo.delete_conversation(conversation_id)
    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversación con id '{conversation_id}' no encontrada",
        )
    return convo





@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def list_conversation_messages(conversation_id: str):
    convo = convo_repo.get_conversation(conversation_id)
    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversación con id '{conversation_id}' no encontrada",
        )
    return msg_repo.list_messages_by_conversation(conversation_id)


class ChatResponse(BaseModel):
    patient_message: MessageResponse
    sarah_message: MessageResponse


@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(conversation_id: str, data: MessageCreate):
    convo = convo_repo.get_conversation(conversation_id)
    if not convo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversación con id '{conversation_id}' no encontrada",
        )

    sender_val = getattr(data, "sender", getattr(data, "sender_type", "patient"))

    return msg_repo.create_message(
        conversation_id=conversation_id,
        sender=sender_val,
        content=data.content,
    )


@router.post("/{conversation_id}/chat", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def chat_with_sarah(conversation_id: str, data: MessageCreate):
    try:
        convo = convo_repo.get_conversation(conversation_id)
        if not convo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversación con id '{conversation_id}' no encontrada",
            )

        # 1. Guardar mensaje del paciente
        patient_msg = msg_repo.create_message(
            conversation_id=conversation_id,
            sender="patient",
            content=data.content,
        )

        # 2. Generar respuesta con el asistente
        sarah_reply_text = generate_sarah_response(
            patient_id=convo.patient_id,
            incoming_message=data.content,
        )

        # 3. Guardar mensaje de Sarah
        sarah_msg = msg_repo.create_message(
            conversation_id=conversation_id,
            sender="sarah",
            content=sarah_reply_text,
        )

        return ChatResponse(
            patient_message=patient_msg,
            sarah_message=sarah_msg,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en chat: {str(e)}"
        )