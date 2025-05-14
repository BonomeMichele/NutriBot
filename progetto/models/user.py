from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    """
    Modello per il profilo dell'utente
    """
    id: str = Field(..., description="ID univoco dell'utente")
    name: Optional[str] = Field(None, description="Nome dell'utente")
    age: Optional[int] = Field(None, description="Età dell'utente")
    gender: Optional[str] = Field(None, description="Genere dell'utente (M/F/Altro)")
    weight: Optional[float] = Field(None, description="Peso in kg")
    height: Optional[float] = Field(None, description="Altezza in cm")
    physical_activity: Optional[str] = Field(None, description="Livello di attività fisica")
    goals: Optional[List[str]] = Field(default=[], description="Obiettivi (es. perdita peso, massa muscolare)")
    dietary_restrictions: Optional[List[str]] = Field(default=[], description="Restrizioni alimentari")
    health_conditions: Optional[List[str]] = Field(default=[], description="Condizioni di salute rilevanti")
    preferences: Optional[List[str]] = Field(default=[], description="Preferenze alimentari")
    created_at: datetime = Field(default_factory=datetime.now, description="Data di creazione")
    updated_at: datetime = Field(default_factory=datetime.now, description="Data di ultimo aggiornamento")
    
    class Config:
        from_attributes = True

class UserSettings(BaseModel):
    """
    Modello per le impostazioni dell'utente
    """
    user_id: str = Field(..., description="ID dell'utente")
    theme: Optional[str] = Field("light", description="Tema dell'interfaccia (light/dark)")
    voice_enabled: bool = Field(False, description="Impostazione per l'output vocale")
    notification_enabled: bool = Field(True, description="Impostazione per le notifiche")
    language: str = Field("it", description="Lingua preferita")
    created_at: datetime = Field(default_factory=datetime.now, description="Data di creazione")
    updated_at: datetime = Field(default_factory=datetime.now, description="Data di ultimo aggiornamento")
    
    class Config:
        from_attributes = True
