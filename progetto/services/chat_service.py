from typing import Dict, Any, List, Optional
import logging
import asyncio
import datetime
import json

from app.core.diet_generator import generate_diet_plan, analyze_nutritional_query
from app.db.chat_repository import save_chat_message, get_chat_history, get_all_chats, delete_chat, delete_all_chats

# Configurazione logging
logger = logging.getLogger(__name__)

async def process_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Elabora un messaggio dell'utente e genera una risposta del chatbot
    
    Args:
        message_data: Dati del messaggio dell'utente
        
    Returns:
        Dizionario con la risposta e i metadati
    """
    try:
        chat_id = message_data.get("chat_id", "")
        message_text = message_data.get("message", "")
        timestamp = message_data.get("timestamp", datetime.datetime.now().isoformat())
        
        # Salva il messaggio dell'utente
        save_chat_message(chat_id, message_text, "user", timestamp)
        
        # Inizia con un messaggio di "sto generando..."
        response_data = {
            "chat_id": chat_id,
            "status": "thinking",
            "message": "Sto analizzando la tua richiesta...",
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Analizza il messaggio per determinare se è una richiesta di dieta
        is_diet_request = _is_diet_request(message_text)
        
        # Genera la risposta in base al tipo di richiesta
        bot_response = ""
        sources = []
        
        if is_diet_request:
            # È una richiesta di dieta, usa il generatore di diete
            diet_result = generate_diet_plan(message_text)
            bot_response = diet_result["diet_plan"]
            sources = diet_result.get("sources", [])
        else:
            # È una domanda generica sulla nutrizione
            analysis_result = analyze_nutritional_query(message_text)
            bot_response = analysis_result["answer"]
            sources = analysis_result.get("sources", [])
        
        # Salva la risposta del bot
        save_chat_message(chat_id, bot_response, "assistant", datetime.datetime.now().isoformat())
        
        # Prepara la risposta finale
        response_data = {
            "chat_id": chat_id,
            "status": "complete",
            "message": bot_response,
            "sources": sources,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return response_data
    except Exception as e:
        logger.error(f"Errore nell'elaborazione del messaggio: {e}")
        return {
            "chat_id": message_data.get("chat_id", ""),
            "status": "error",
            "message": f"Mi dispiace, si è verificato un errore: {str(e)}",
            "timestamp": datetime.datetime.now().isoformat()
        }

def _is_diet_request(message: str) -> bool:
    """
    Determina se un messaggio è una richiesta di dieta
    
    Args:
        message: Il testo del messaggio
        
    Returns:
        True se il messaggio è una richiesta di dieta, False altrimenti
    """
    # Parole chiave che potrebbero indicare una richiesta di dieta
    diet_keywords = [
        "dieta", "piano alimentare", "nutrizione", "regime alimentare",
        "menu settimanale", "pasti", "calorie", "mangiare", "alimentazione",
        "peso", "dimagrire", "ingrassare", "massa muscolare", "proteina"
    ]
    
    # Frasi comuni per richieste di dieta
    diet_phrases = [
        "voglio perdere peso", "vorrei dimagrire", "come posso aumentare di peso",
        "che cosa dovrei mangiare", "cosa posso mangiare", "come dovrei alimentarmi",
        "sono un uomo di", "sono una donna di", "ho anni", "sono alto", "sono alta",
        "il mio obiettivo è", "voglio mettere massa", "sedentario", "attivo", "sportivo"
    ]
    
    # Converti il messaggio in minuscolo per un confronto case-insensitive
    message_lower = message.lower()
    
    # Controlla se il messaggio contiene almeno una parola chiave e una frase comune
    has_keyword = any(keyword in message_lower for keyword in diet_keywords)
    has_phrase = any(phrase in message_lower for phrase in diet_phrases)
    
    # Se il messaggio è lungo e contiene una parola chiave o una frase, consideralo una richiesta di dieta
    # Le richieste di dieta tendono ad essere più lunghe di semplici domande
    is_long_message = len(message.split()) >= 10
    
    return (has_keyword and (has_phrase or is_long_message))

def get_chat_history_formatted(chat_id: str) -> List[Dict[str, Any]]:
    """
    Recupera la cronologia della chat formattata per il frontend
    
    Args:
        chat_id: L'ID della chat
        
    Returns:
        Una lista di dizionari con i messaggi formattati
    """
    history = get_chat_history(chat_id)
    formatted_history = []
    
    for message in history:
        formatted_message = {
            "role": message.role,
            "content": message.content,
            "timestamp": message.timestamp
        }
        formatted_history.append(formatted_message)
    
    return formatted_history
