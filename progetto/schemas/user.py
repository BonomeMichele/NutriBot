from pydantic import BaseModel
from typing import List, Optional

class UserProfileRequest(BaseModel):
    """Schema per le richieste con profilo utente"""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    physical_activity: Optional[str] = None
    goals: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    health_conditions: Optional[List[str]] = None
    preferences: Optional[List[str]] = None

class UserProfileResponse(BaseModel):
    """Schema per le risposte con profilo utente"""
    id: str
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    physical_activity: Optional[str] = None
    goals: Optional[List[str]] = []
    dietary_restrictions: Optional[List[str]] = []
    health_conditions: Optional[List[str]] = []
    preferences: Optional[List[str]] = []
    success: bool
    message: str
