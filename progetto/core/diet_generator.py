from typing import Dict, Any, List, Optional
import logging
from openai import OpenAI
from app.config import settings
from app.core.rag_engine import query_rag

# Configurazione logging
logger = logging.getLogger(__name__)

# Client OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_diet_plan(user_profile: str) -> Dict[str, Any]:
    """
    Genera un piano dietetico personalizzato basato sul profilo utente
    e sul contesto recuperato dal motore RAG
    
    Args:
        user_profile: Il profilo utente con informazioni demografiche e obiettivi
    
    Returns:
        Un dizionario contenente la dieta generata e metadati
    """
    try:
        # Recupera informazioni rilevanti dal motore RAG
        rag_results = query_rag(user_profile)
        context = rag_results["context"]
        
        # Prepara il prompt per il modello
        prompt = settings.DIET_USER_PROMPT_TEMPLATE.format(
            user_profile=user_profile,
            context=context
        )
        
        # Genera la dieta con il modello GPT-4
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": settings.DIET_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Estrai la risposta generata
        diet_text = response.choices[0].message.content
        
        return {
            "user_profile": user_profile,
            "diet_plan": diet_text,
            "tokens_used": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "sources": [node.node.metadata.get("file_name", "documento CREA/LARN") 
                       for node in rag_results.get("source_nodes", [])]
        }
    except Exception as e:
        logger.error(f"Errore nella generazione della dieta: {e}")
        raise

def analyze_nutritional_query(query: str) -> Dict[str, Any]:
    """
    Analizza una query nutrizionale e fornisce una risposta informativa
    utilizzando il motore RAG e GPT-4
    
    Args:
        query: La domanda o richiesta dell'utente
        
    Returns:
        Un dizionario contenente la risposta e metadati
    """
    try:
        # Recupera informazioni rilevanti dal motore RAG
        rag_results = query_rag(query)
        context = rag_results["context"]
        
        # Prepara il prompt sistema per il modello
        system_prompt = """
        Sei un nutrizionista esperto italiano che fornisce consigli basati sulle linee guida ufficiali italiane.
        Rispondi alle domande sulla nutrizione in modo chiaro, accurato e utile, basandoti solo sui contenuti
        forniti come contesto. Se non hai informazioni sufficienti, indica quali informazioni mancano.
        Cita sempre le tue fonti (LARN, INRAN, CREA) quando opportuno.
        """
        
        # Prepara il prompt utente
        user_prompt = f"""
        Domanda dell'utente: {query}
        
        Contesto rilevante:
        {context}
        
        Rispondi alla domanda dell'utente in modo chiaro e conciso, basandoti sulle informazioni fornite.
        Cita le fonti quando appropriato.
        """
        
        # Genera la risposta con il modello
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        # Estrai la risposta generata
        answer_text = response.choices[0].message.content
        
        return {
            "query": query,
            "answer": answer_text,
            "tokens_used": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "sources": [node.node.metadata.get("file_name", "documento CREA/LARN") 
                       for node in rag_results.get("source_nodes", [])]
        }
    except Exception as e:
        logger.error(f"Errore nell'analisi della query nutrizionale: {e}")
        raise
