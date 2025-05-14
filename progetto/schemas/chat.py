from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    """Schema per i messaggi di chat"""
    chat_id: str
    role: str  # "user" o "assistant"
    content: str
    timestamp: str
    
class ChatSession(BaseModel):
    """Schema per le sessioni di chat"""
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int
