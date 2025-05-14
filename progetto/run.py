import os
import logging
import uvicorn
from app.main import app
from app.config import settings

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    """
    Funzione principale per avviare l'applicazione
    """
    # Verifica che le directory necessarie esistano
    if not os.path.exists(settings.DOCUMENTS_DIR):
        os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
        logger.info(f"Creata directory per i documenti: {settings.DOCUMENTS_DIR}")
    
    if not os.path.exists(settings.VECTORSTORE_PATH):
        os.makedirs(settings.VECTORSTORE_PATH, exist_ok=True)
        logger.info(f"Creata directory per il vectorstore: {settings.VECTORSTORE_PATH}")
    
    # Verifica la chiave API OpenAI
    if not settings.OPENAI_API_KEY:
        logger.warning("⚠️ OPENAI_API_KEY non trovata nelle variabili d'ambiente.")
        logger.warning("Crea un file .env nella directory principale con la tua API key di OpenAI:")
        logger.warning("OPENAI_API_KEY=sk-your-api-key")
    
    # Avvia il server
    logger.info("🚀 Avvio del server Chatbot Nutrizionista")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
