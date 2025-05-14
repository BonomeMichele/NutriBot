import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class Settings(BaseSettings):
    # Cartella di base
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    # OpenAI API
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Modelli
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4"
    
    # Paths dei documenti
    DOCUMENTS_DIR: Path = Path(__file__).resolve().parent / "static" / "documents"
    
    # Vectorstore
    VECTORSTORE_PATH: Path = Path(__file__).resolve().parent / "db" / "vectorstore"
    
    # Configurazioni di RAG
    TOP_K_RESULTS: int = 5  # Numero di documenti più rilevanti da recuperare
    
    # Prompt templates per la generazione di diete
    DIET_SYSTEM_PROMPT: str = """
    Sei un nutrizionista esperto italiano specializzato nella creazione di diete personalizzate.
    Utilizzerai le informazioni scientifiche ufficiali fornite dai documenti LARN, INRAN e CREA per creare diete bilanciate.
    Considera sempre l'età, il sesso, il livello di attività fisica e le eventuali esigenze o restrizioni alimentari.
    Le tue risposte devono essere professionali ma facilmente comprensibili da persone non esperte.
    """
    
    DIET_USER_PROMPT_TEMPLATE: str = """
    Crea una dieta settimanale personalizzata basata sulle seguenti informazioni:
    
    Profilo dell'utente: {user_profile}
    
    Informazioni nutrizionali rilevanti:
    {context}
    
    Genera una dieta settimanale con 3 pasti al giorno (colazione, pranzo, cena) e 2 spuntini (metà mattina e metà pomeriggio).
    Per ogni pasto indica:
    1. Gli alimenti raccomandati con relative quantità
    2. L'apporto calorico approssimativo
    3. Brevi suggerimenti pratici per la preparazione
    
    Alla fine della dieta settimanale, aggiungi:
    - I principi nutrizionali seguiti
    - Consigli generali per il mantenimento
    - Le fonti scientifiche utilizzate (LARN, INRAN, CREA)
    
    Formatta la risposta in modo chiaro e leggibile, usando elenchi puntati quando appropriato.
    """
    
    # Chiave per il widget Eleven Labs
    ELEVENLABS_AGENT_ID: str = "81R2UL4OJFryMGXHQIth"

# Istanzia le impostazioni
settings = Settings()

# Assicurati che le directory necessarie esistano
os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
os.makedirs(settings.VECTORSTORE_PATH, exist_ok=True)
