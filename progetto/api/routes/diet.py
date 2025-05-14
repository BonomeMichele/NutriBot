from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging

from app.core.diet_generator import generate_diet_plan, analyze_nutritional_query
from app.schemas.diet import DietRequest, DietResponse

# Configurazione logging
logger = logging.getLogger(__name__)

# Creazione del router
router = APIRouter(
    prefix="/diet",
    tags=["diet"],
    responses={404: {"description": "Non trovato"}},
)

@router.post("/generate", response_model=DietResponse)
async def create_diet_plan(diet_request: DietRequest):
    """
    Genera un piano dietetico personalizzato basato sul profilo utente
    """
    try:
        # Genera la dieta personalizzata
        diet_result = generate_diet_plan(diet_request.user_profile)
        
        # Restituisci la risposta
        return DietResponse(
            user_profile=diet_request.user_profile,
            diet_plan=diet_result["diet_plan"],
            sources=diet_result.get("sources", []),
            success=True,
            message="Dieta generata con successo"
        )
    except Exception as e:
        logger.error(f"Errore nella generazione della dieta: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nella generazione della dieta: {str(e)}")

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_nutrition_query(query: str = Body(..., embed=True)):
    """
    Analizza una query nutrizionale e fornisce una risposta informativa
    """
    try:
        # Analizza la query nutrizionale
        analysis_result = analyze_nutritional_query(query)
        
        # Restituisci la risposta
        return {
            "query": query,
            "answer": analysis_result["answer"],
            "sources": analysis_result.get("sources", []),
            "success": True,
            "message": "Analisi completata con successo"
        }
    except Exception as e:
        logger.error(f"Errore nell'analisi della query nutrizionale: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nell'analisi: {str(e)}")

@router.get("/recommendations/{category}", response_model=Dict[str, Any])
async def get_recommendations(category: str):
    """
    Ottiene raccomandazioni nutrizionali per una specifica categoria
    (es: proteine, carboidrati, vitamine, etc.)
    """
    try:
        # Analizza la query per la categoria
        query = f"Quali sono le raccomandazioni nutrizionali per {category} secondo le linee guida italiane?"
        analysis_result = analyze_nutritional_query(query)
        
        # Restituisci la risposta
        return {
            "category": category,
            "recommendations": analysis_result["answer"],
            "sources": analysis_result.get("sources", []),
            "success": True
        }
    except Exception as e:
        logger.error(f"Errore nel recupero delle raccomandazioni: {e}")
        raise HTTPException(status_code=500, detail=f"Errore nel recupero delle raccomandazioni: {str(e)}")
