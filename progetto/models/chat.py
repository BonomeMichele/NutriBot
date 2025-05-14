from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ChatMessageModel(BaseModel):
    """
    Modello per i messaggi di chat
    """
    id: str = Field(..., description="ID univoco del messaggio")
    chat_id: str = Field(..., description="ID della chat a cui appartiene il messaggio")
    role: str = Field(..., description="Ruolo del mittente (user o assistant)")
    content: str = Field(..., description="Contenuto del messaggio")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del messaggio")
    
    class Config:
        from_attributes = True

class ChatModel(BaseModel):
    """
    Modello per le chat
    """
    id: str = Field(..., description="ID univoco della chat")
    title: str = Field(..., description="Titolo della chat")
    created_at: datetime = Field(default_factory=datetime.now, description="Data di creazione")
    updated_at: datetime = Field(default_factory=datetime.now, description="Data di ultimo aggiornamento")
    messages: Optional[List[ChatMessageModel]] = Field(default=[], description="Lista dei messaggi nella chat")
    
    class Config:
        from_attributes = True
