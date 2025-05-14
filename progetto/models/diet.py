from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class MealItem(BaseModel):
    """
    Modello per un singolo alimento in un pasto
    """
    name: str = Field(..., description="Nome dell'alimento")
    quantity: str = Field(..., description="Quantità (es. '100g', '1 porzione')")
    calories: Optional[int] = Field(None, description="Calorie approssimative")
    
    class Config:
        from_attributes = True

class Meal(BaseModel):
    """
    Modello per un pasto
    """
    name: str = Field(..., description="Nome del pasto (es. 'Colazione', 'Pranzo')")
    items: List[MealItem] = Field(..., description="Alimenti nel pasto")
    total_calories: Optional[int] = Field(None, description="Calorie totali del pasto")
    notes: Optional[str] = Field(None, description="Note o suggerimenti per il pasto")
    
    class Config:
        from_attributes = True

class DailyPlan(BaseModel):
    """
    Modello per un piano giornaliero
    """
    day: str = Field(..., description="Giorno della settimana")
    meals: List[Meal] = Field(..., description="Pasti del giorno")
    total_calories: Optional[int] = Field(None, description="Calorie totali giornaliere")
    notes: Optional[str] = Field(None, description="Note o suggerimenti per la giornata")
    
    class Config:
        from_attributes = True

class DietPlan(BaseModel):
    """
    Modello per un piano dietetico completo
    """
    id: str = Field(..., description="ID univoco del piano dietetico")
    title: str = Field(..., description="Titolo del piano dietetico")
    user_profile: str = Field(..., description="Profilo dell'utente per cui è stata generata la dieta")
    created_at: datetime = Field(default_factory=datetime.now, description="Data di creazione")
    daily_plans: List[DailyPlan] = Field(..., description="Piani giornalieri")
    nutritional_principles: Optional[str] = Field(None, description="Principi nutrizionali seguiti")
    general_recommendations: Optional[str] = Field(None, description="Raccomandazioni generali")
    sources: List[str] = Field(default=[], description="Fonti utilizzate per la generazione della dieta")
    
    class Config:
        from_attributes = True
