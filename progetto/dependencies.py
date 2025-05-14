# Dipendenze condivise per FastAPI

from typing import Dict, Any
from fastapi import Depends, Header, HTTPException, status
import logging

# Configurazione logging
logger = logging.getLogger(__name__)

async def get_api_key(x_api_key: str = Header(None)):
    """
    Middleware per la verifica dell'API key nelle richieste API
    Utile per proteggere gli endpoint API pubblici
    
    Args:
        x_api_key: L'API key fornita nell'header
        
    Returns:
        L'API key se valida
        
    Raises:
        HTTPException: Se l'API key non è valida o non è fornita
    """
    # Nella versione di produzione, dovresti verificare l'API key con un sistema più sicuro
    # Per ora, questa è solo un'implementazione di esempio
    if x_api_key is not None:
        return x_api_key
    else:
        # In modalità di sviluppo, non richiedere l'API key
        # In produzione, decommentare la riga seguente
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key mancante o non valida")
        return None

async def get_token_header(x_token: str = Header(None)):
    """
    Middleware per la verifica del token nelle richieste API
    Utile per gestire l'autenticazione degli utenti
    
    Args:
        x_token: Il token fornito nell'header
        
    Returns:
        Il token se valido
        
    Raises:
        HTTPException: Se il token non è valido o non è fornito
    """
    # Nella versione di produzione, dovresti verificare il token con un sistema di autenticazione
    # Per ora, questa è solo un'implementazione di esempio
    if x_token is not None:
        return x_token
    else:
        # In modalità di sviluppo, non richiedere il token
        # In produzione, decommentare la riga seguente
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token mancante o non valido")
        return None

def get_query_params(q: str = None):
    """
    Middleware per gestire i parametri di query
    
    Args:
        q: Il parametro di query
        
    Returns:
        Un dizionario con i parametri di query
    """
    return {"q": q}
