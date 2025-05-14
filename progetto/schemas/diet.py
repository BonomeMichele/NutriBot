from pydantic import BaseModel
from typing import List, Optional

class DietRequest(BaseModel):
    """Schema per le richieste di generazione dieta"""
    user_profile: str
    
class DietResponse(BaseModel):
    """Schema per le risposte con diete generate"""
    user_profile: str
    diet_plan: str
    sources: List[str] = []
    success: bool
    message: str
