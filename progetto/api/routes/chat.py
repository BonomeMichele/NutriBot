from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import uuid
import datetime
import logging

from app.services.chat_service import (
    get_chat_history,
    save_chat_message,
    delete_chat,
    delete_all_chats,
    process_message as service_process_message
)
from app.schemas.chat import ChatMessage, ChatSession

# Configurazione logging
logger = logging.getLogger(__name__)

# Creazione del router
router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Non trovato"}},
)

class MessageRequest(BaseModel):
    """Schema per le richieste di messaggi"""
    chat_id: Optional[str] = None
    message: str
    timestamp: Optional[str] = None

class ChatListResponse(BaseModel):
    """Schema per la risposta con la lista delle chat"""
    chats: List[ChatSession]

@router.post("/message", response_model=Dict[str, Any])
async def send_message(message_request: MessageRequest):
    """
    Endpoint per inviare un messaggio al chatbot e ricevere una risposta
    """
    try:
        # Genera un chat_id se non è fornito
        chat_id = message_request.chat_id or str(uuid.uuid4())
        
        # Timestamp corrente se non fornito
        timestamp = message_request.timestamp or datetime.datetime.now().isoformat()
        
        # Processa il messaggio attraverso il service
        response = await service_process_message({
            "chat_id": chat_id,
            "message": message_request.message,
            "timestamp": timestamp
        })
        
        return response
    except Exception as e:
        logger.error(f"Errore nell'elaborazione del messaggio: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nell'elaborazione del messaggio: {str(e)}")

@router.get("/history/{chat_id}", response_model=List[ChatMessage])
async def get_history(chat_id: str):
    """
    Recupera la cronologia dei messaggi per una specifica chat
    """
    try:
        history = get_chat_history(chat_id)
        return history
    except Exception as e:
        logger.error(f"Errore nel recupero della cronologia chat: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel recupero della cronologia: {str(e)}")

@router.get("/list", response_model=ChatListResponse)
async def list_chats():
    """
    Recupera l'elenco di tutte le chat salvate
    """
    try:
        from app.db.chat_repository import get_all_chats
        chats = get_all_chats()
        return ChatListResponse(chats=chats)
    except Exception as e:
        logger.error(f"Errore nel recupero dell'elenco chat: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel recupero dell'elenco chat: {str(e)}")

@router.delete("/{chat_id}", response_model=Dict[str, str])
async def remove_chat(chat_id: str):
    """
    Elimina una specifica chat
    """
    try:
        delete_chat(chat_id)
        return {"status": "success", "message": f"Chat {chat_id} eliminata con successo"}
    except Exception as e:
        logger.error(f"Errore nell'eliminazione della chat: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nell'eliminazione della chat: {str(e)}")

@router.delete("/", response_model=Dict[str, str])
async def remove_all_chats():
    """
    Elimina tutte le chat
    """
    try:
        delete_all_chats()
        return {"status": "success", "message": "Tutte le chat sono state eliminate con successo"}
    except Exception as e:
        logger.error(f"Errore nell'eliminazione di tutte le chat: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nell'eliminazione di tutte le chat: {str(e)}")

# Funzione per processare i messaggi (utilizzata sia dall'API che dal WebSocket)
async def process_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Elabora un messaggio e genera una risposta utilizzando il servizio chat
    """
    try:
        response = await service_process_message(message_data)
        return response
    except Exception as e:
        logger.error(f"Errore nell'elaborazione del messaggio: {e}")
        return {
            "status": "error",
            "message": f"Errore nell'elaborazione del messaggio: {str(e)}",
            "chat_id": message_data.get("chat_id", "")
        }
