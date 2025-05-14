from typing import Dict, Any, List, Optional
import logging
from app.core.diet_generator import generate_diet_plan

# Configurazione logging
logger = logging.getLogger(__name__)

async def generate_diet(user_profile: str) -> Dict[str, Any]:
    """
    Genera una dieta personalizzata basata sul profilo dell'utente
    
    Args:
        user_profile: Il profilo dell'utente con informazioni demografiche e obiettivi
        
    Returns:
        Un dizionario con il piano dietetico e metadati
    """
    try:
        # Genera la dieta utilizzando il core generator
        diet_result = generate_diet_plan(user_profile)
        
        # Formatta la risposta
        response = {
            "user_profile": user_profile,
            "diet_plan": diet_result["diet_plan"],
            "sources": diet_result.get("sources", []),
            "success": True,
            "message": "Dieta generata con successo"
        }
        
        return response
    except Exception as e:
        logger.error(f"Errore nella generazione della dieta: {e}")
        return {
            "user_profile": user_profile,
            "diet_plan": "",
            "sources": [],
            "success": False,
            "message": f"Errore nella generazione della dieta: {str(e)}"
        }

def format_diet_for_display(diet_data: Dict[str, Any]) -> str:
    """
    Formatta i dati della dieta per la visualizzazione nel chatbot
    
    Args:
        diet_data: I dati della dieta generata
        
    Returns:
        Una stringa formattata per la visualizzazione
    """
    diet_plan = diet_data.get("diet_plan", "")
    sources = diet_data.get("sources", [])
    
    # La dieta è già formattata dal generatore, aggiungiamo solo le fonti
    formatted_diet = diet_plan
    
    if sources:
        sources_text = "\n\n**Fonti consultate:**\n"
        for source in sources:
            sources_text += f"- {source}\n"
        formatted_diet += sources_text
    
    return formatted_diet
