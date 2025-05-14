from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os
import logging
from pathlib import Path

from app.schemas.chat import ChatMessage, ChatSession
from app.config import settings

# Configurazione logging
logger = logging.getLogger(__name__)

# Percorso del file di database
DB_DIR = Path(__file__).resolve().parent / "data"
CHATS_FILE = DB_DIR / "chats.json"

# Assicurati che la directory esista
os.makedirs(DB_DIR, exist_ok=True)

def _load_chats() -> Dict[str, Any]:
    """
    Carica le chat dal file JSON
    
    Returns:
        Un dizionario con le chat caricate
    """
    if not os.path.exists(CHATS_FILE):
        return {"chats": {}}
    
    try:
        with open(CHATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Errore nel caricamento delle chat: {e}")
        return {"chats": {}}

def _save_chats(chats_data: Dict[str, Any]) -> None:
    """
    Salva le chat nel file JSON
    
    Args:
        chats_data: Il dizionario delle chat da salvare
    """
    try:
        with open(CHATS_FILE, "w", encoding="utf-8") as f:
            json.dump(chats_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Errore nel salvataggio delle chat: {e}")
        raise

def get_chat_history(chat_id: str) -> List[ChatMessage]:
    """
    Recupera lo storico messaggi di una chat
    
    Args:
        chat_id: L'ID della chat
        
    Returns:
        Una lista di messaggi
    """
    chats_data = _load_chats()
    
    if chat_id not in chats_data["chats"]:
        return []
    
    # Converti i dati grezzi in oggetti ChatMessage
    messages = []
    for msg_data in chats_data["chats"][chat_id]["messages"]:
        messages.append(ChatMessage(**msg_data))
    
    return messages

def save_chat_message(chat_id: str, message: str, role: str, timestamp: Optional[str] = None) -> None:
    """
    Salva un messaggio in una chat
    
    Args:
        chat_id: L'ID della chat
        message: Il contenuto del messaggio
        role: Il ruolo (user o assistant)
        timestamp: Il timestamp del messaggio (opzionale)
    """
    chats_data = _load_chats()
    
    # Se la chat non esiste, creala
    if chat_id not in chats_data["chats"]:
        chats_data["chats"][chat_id] = {
            "id": chat_id,
            "title": f"Chat {len(chats_data['chats']) + 1}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": []
        }
    
    # Aggiorna il timestamp dell'ultima modifica
    chats_data["chats"][chat_id]["updated_at"] = datetime.now().isoformat()
    
    # Se è il primo messaggio dell'utente, usa parte del testo come titolo
    if role == "user" and len(chats_data["chats"][chat_id]["messages"]) == 0:
        title = message[:30] + "..." if len(message) > 30 else message
        chats_data["chats"][chat_id]["title"] = title
    
    # Crea il nuovo messaggio
    new_message = {
        "chat_id": chat_id,
        "role": role,
        "content": message,
        "timestamp": timestamp or datetime.now().isoformat(),
    }
    
    # Aggiungi il messaggio alla chat
    chats_data["chats"][chat_id]["messages"].append(new_message)
    
    # Salva le modifiche
    _save_chats(chats_data)

def delete_chat(chat_id: str) -> None:
    """
    Elimina una chat
    
    Args:
        chat_id: L'ID della chat da eliminare
    """
    chats_data = _load_chats()
    
    if chat_id in chats_data["chats"]:
        del chats_data["chats"][chat_id]
        _save_chats(chats_data)

def delete_all_chats() -> None:
    """
    Elimina tutte le chat
    """
    _save_chats({"chats": {}})

def get_all_chats() -> List[ChatSession]:
    """
    Recupera tutte le sessioni di chat
    
    Returns:
        Una lista di tutte le sessioni di chat
    """
    chats_data = _load_chats()
    
    # Converti i dati grezzi in oggetti ChatSession
    chat_sessions = []
    for chat_id, chat_data in chats_data["chats"].items():
        session = ChatSession(
            id=chat_id,
            title=chat_data["title"],
            created_at=chat_data["created_at"],
            updated_at=chat_data["updated_at"],
            message_count=len(chat_data["messages"])
        )
        chat_sessions.append(session)
    
    # Ordina per data di aggiornamento (più recente prima)
    chat_sessions.sort(key=lambda x: x.updated_at, reverse=True)
    
    return chat_sessions

def update_chat_title(chat_id: str, new_title: str) -> None:
    """
    Aggiorna il titolo di una chat
    
    Args:
        chat_id: L'ID della chat
        new_title: Il nuovo titolo
    """
    chats_data = _load_chats()
    
    if chat_id in chats_data["chats"]:
        chats_data["chats"][chat_id]["title"] = new_title
        _save_chats(chats_data)
