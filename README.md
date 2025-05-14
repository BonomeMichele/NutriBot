# Chatbot Nutrizionista con RAG

Un chatbot specializzato in nutrizione che genera diete personalizzate basate su RAG (Retrieval-Augmented Generation) utilizzando documenti ufficiali italiani.

## Caratteristiche

- 🥗 Generazione di diete personalizzate in base al profilo dell'utente
- 📑 Sistema RAG per recuperare informazioni dai documenti ufficiali (LARN, INRAN, CREA)
- 💬 Interfaccia chat reattiva e moderna
- 🔊 Supporto per output vocale con ElevenLabs
- 📱 Responsive design per dispositivi mobili
- 🔍 Ricerca contestuale per domande nutrizionali

## Requisiti

- Python 3.8+
- FastAPI
- Llama-Index
- OpenAI API Key
- ElevenLabs (opzionale, per la funzionalità vocale)

## Installazione

1. Clona il repository:

```bash
git clone https://github.com/tuorepository/chatbot-nutrizionista.git
cd chatbot-nutrizionista
```

2. Crea un ambiente virtuale e attivalo:

```bash
python -m venv venv
# Su Windows
venv\Scripts\activate
# Su Linux/Mac
source venv/bin/activate
```

3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

4. Crea un file `.env` nella directory principale con la tua API key di OpenAI:

```
OPENAI_API_KEY=sk-your-api-key
```

5. Prepara i documenti:
   
Crea una directory `app/static/documents` e inserisci i documenti nutrizionali (PDF, DOCX, TXT) che desideri utilizzare per il sistema RAG. Puoi scaricare i documenti ufficiali dal sito del CREA (https://www.crea.gov.it/).

## Esecuzione

Avvia l'applicazione con il seguente comando:

```bash
python run.py
```

Oppure in modalità sviluppo:

```bash
uvicorn app.main:app --reload
```

L'applicazione sarà disponibile all'indirizzo `http://localhost:8000`.

## Struttura del Progetto

```
/chatbot-nutrizionista/
│
├── app/                            # Directory principale dell'applicazione
│   ├── __init__.py                 # Inizializzatore pacchetto Python
│   ├── main.py                     # Entry point FastAPI 
│   ├── config.py                   # Configurazioni dell'applicazione
│   ├── dependencies.py             # Dipendenze condivise
│   │
│   ├── api/                        # API endpoints
│   │   ├── __init__.py
│   │   ├── routes/                 # Route API
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # Endpoint per gestione chat
│   │   │   └── diet.py             # Endpoint per generazione diete
│   │
│   ├── core/                       # Logica di business core
│   │   ├── __init__.py
│   │   ├── rag_engine.py           # Motore RAG
│   │   ├── diet_generator.py       # Generatore di diete
│   │   └── llm_manager.py          # Gestione interazioni con OpenAI
│   │
│   ├── db/                         # Layer di accesso ai dati
│   │   ├── __init__.py
│   │   ├── chat_repository.py      # Operazioni su chat
│   │   └── vectorstore.py          # Gestione del vectorstore
│   │
│   ├── models/                     # Modelli dati
│   │   ├── __init__.py
│   │   ├── chat.py                 # Modelli per chat
│   │   ├── diet.py                 # Modelli per diete
│   │   └── user.py                 # Modelli per utenti
│   │
│   ├── schemas/                    # Schemi Pydantic
│   │   ├── __init__.py
│   │   ├── chat.py                 # Schema per chat
│   │   ├── diet.py                 # Schema per diete
│   │   └── user.py                 # Schema per utenti
│   │
│   ├── services/                   # Servizi business logic
│   │   ├── __init__.py
│   │   ├── chat_service.py         # Servizio per gestione chat
│   │   └── diet_service.py         # Servizio per generazione diete
│   │
│   ├── static/                     # File statici
│   │   ├── js/                     # JavaScript
│   │   │   └── chat.js             # Script per gestione chat frontend
│   │   └── documents/              # Documenti nutrizionali
│   │
│   └── templates/                  # Template HTML
│       └── index.html              # Template principale
│
├── .env                           # Variabili d'ambiente
├── .gitignore                     # File da ignorare in git
├── requirements.txt               # Dipendenze del progetto
├── README.md                      # Documentazione progetto
└── run.py                         # Script per avviare l'applicazione
```

## Utilizzo dell'API

### Endpoint API

- `GET /` - Pagina principale del chatbot
- `POST /api/chat/message` - Invia un messaggio al chatbot
- `GET /api/chat/history/{chat_id}` - Recupera la cronologia di una chat
- `GET /api/chat/list` - Elenca tutte le chat salvate
- `DELETE /api/chat/{chat_id}` - Elimina una chat specifica
- `DELETE /api/chat/` - Elimina tutte le chat
- `POST /api/diet/generate` - Genera una dieta personalizzata
- `POST /api/diet/analyze` - Analizza una query nutrizionale
- `GET /api/diet/recommendations/{category}` - Ottiene raccomandazioni per una categoria

### Esempio di richiesta per generare una dieta

```bash
curl -X POST "http://localhost:8000/api/diet/generate" \
  -H "Content-Type: application/json" \
  -d '{"user_profile": "Sono un uomo di 35 anni, peso 80kg, sono alto 178cm e faccio attività fisica 3 volte a settimana. Vorrei una dieta per perdere peso."}'
```

## Licenza

MIT

## Contatti

Per domande o segnalazioni di problemi, aprire un issue su GitHub.
