from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
import logging
from pathlib import Path

from app.api.routes import chat, diet
from app.core.rag_engine import initialize_rag_engine
from app.config import settings

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Inizializzazione app FastAPI
app = FastAPI(
    title="Chatbot Nutrizionista",
    description="Un chatbot specializzato in nutrizione che genera diete personalizzate basate su RAG",
    version="1.0.0",
)

# Monta le route API
app.include_router(chat.router, prefix="/api")
app.include_router(diet.router, prefix="/api")

# Configurazione delle directory statiche e dei template
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Inizializzazione del motore RAG all'avvio dell'app
@app.on_event("startup")
async def startup_event():
    try:
        # Inizializza il motore RAG
        logger.info("Inizializzazione del motore RAG...")
        initialize_rag_engine()
        logger.info("Motore RAG inizializzato con successo!")
    except Exception as e:
        logger.error(f"Errore durante l'inizializzazione del motore RAG: {e}")
        # Non arrestare l'app, ma segnala l'errore
        pass

# Endpoint root che serve la pagina HTML principale
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket per la comunicazione in tempo reale con il frontend
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Processa i dati ricevuti
            message_data = json.loads(data)
            response = await chat.process_message(message_data)
            # Invia la risposta al client
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        logger.info("Cliente WebSocket disconnesso")
    except Exception as e:
        logger.error(f"Errore WebSocket: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    # Avvio del server
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
