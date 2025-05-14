from typing import Dict, Any, List, Optional
from openai import OpenAI
import logging

from app.config import settings

# Configurazione logging
logger = logging.getLogger(__name__)

# Client OpenAI
client = None

def get_openai_client():
    """
    Restituisce un'istanza del client OpenAI
    
    Returns:
        Il client OpenAI configurato
    """
    global client
    
    # Se il client non è stato inizializzato, lo inizializza
    if client is None:
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception as e:
            logger.error(f"Errore nell'inizializzazione del client OpenAI: {e}")
            raise
    
    return client

def generate_chat_completion(prompt: str, system_prompt: str = None, temperature: float = 0.7) -> Dict[str, Any]:
    """
    Genera una risposta utilizzando il modello chat GPT
    
    Args:
        prompt: Il prompt dell'utente
        system_prompt: Il prompt di sistema (opzionale)
        temperature: La temperatura per la generazione (default: 0.7)
        
    Returns:
        Un dizionario con la risposta e i metadati
    """
    try:
        # Ottieni il client OpenAI
        openai_client = get_openai_client()
        
        # Prepara i messaggi
        messages = []
        
        # Aggiungi il prompt di sistema se fornito
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Aggiungi il prompt dell'utente
        messages.append({"role": "user", "content": prompt})
        
        # Genera la risposta
        response = openai_client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Estrai la risposta generata
        generated_text = response.choices[0].message.content
        
        return {
            "text": generated_text,
            "tokens_used": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        logger.error(f"Errore nella generazione della risposta: {e}")
        raise
