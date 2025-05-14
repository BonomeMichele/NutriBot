🥦 __NutriBot – Chatbot Nutrizionale con RAG__

Un assistente virtuale specializzato in nutrizione che sfrutta la potenza del Retrieval-Augmented Generation (RAG) e documentazione scientifica ufficiale per generare diete personalizzate e rispondere a domande nutrizionali in linguaggio naturale.

📋 __Panoramica__

NutriBot è un'applicazione web conversazionale costruita con FastAPI, LlamaIndex e modelli linguistici OpenAI, progettata per fornire consigli alimentari affidabili e personalizzati sulla base delle linee guida italiane ufficiali (LARN, INRAN, CREA).

🔑 __Caratteristiche principali__

🥗 __Chatbot Nutrizionale__

Generazione automatica di piani alimentari personalizzati

Analisi nutrizionale su richiesta dell'utente

Risposte basate su documenti scientifici grazie al motore RAG

Comprensione del profilo dell’utente (età, peso, altezza, obiettivi)

Output testuale e vocale (opzionale) grazie a ElevenLabs

💬 __Interfaccia Utente__

UI responsive e moderna

Chat interattiva in tempo reale

Integrazione con JavaScript per una user experience fluida

📁 __Documentazione e fonti__

Supporto per documenti nutrizionali ufficiali (PDF, DOCX, TXT)

Parsing, indicizzazione e interrogazione semantica tramite LlamaIndex

🧠 __Backend Intelligente__

Motore RAG avanzato con vector store interno

Modularità completa: API, logica business, repository dati

Supporto per cronologia chat e gestione utenti


🚀 __Installazione__

__Prerequisiti__

Python 3.8+

OpenAI API Key

(Opzionale) Chiave API ElevenLabs

--Clona il repository

git clone https://github.com/BonomeMichele/NutriBot.git
cd NutriBot

--Crea e attiva un ambiente virtuale

python -m venv venv

Windows
venv\Scripts\activate

macOS/Linux
source venv/bin/activate

--Installa le dipendenze

pip install -r requirements.txt

--Crea un file .env con la tua chiave API OpenAI:

OPENAI_API_KEY=sk-xxx

(opzionale)
ELEVENLABS_API_KEY=xxx

--Inserisci i documenti nutrizionali

Apri la cartella:

mkdir -p app/static/documents

Inserisci qui PDF, DOCX o TXT dei documenti ufficiali (LARN, CREA, INRAN).

🧪 __Avvio dell’applicazione__

Modalità standard:

python run.py

Modalità sviluppo:

uvicorn app.main:app --reload

L'app sarà accessibile su http://localhost:8000

📡 __API Endpoints__

🔁 __Chat__

POST /api/chat/message – Invia un messaggio al chatbot

GET /api/chat/history/{chat_id} – Recupera la cronologia

GET /api/chat/list – Elenco delle chat salvate

DELETE /api/chat/{chat_id} – Elimina una chat

DELETE /api/chat/ – Elimina tutte le chat

🥗 __Dieta__

POST /api/diet/generate – Genera una dieta personalizzata

POST /api/diet/analyze – Risponde a domande nutrizionali

GET /api/diet/recommendations/{category} – Raccomandazioni per categoria

📨 __Esempio: Generazione dieta__

curl -X POST http://localhost:8000/api/diet/generate

-H "Content-Type: application/json"

-d '{"user_profile": "Sono una donna di 30 anni, 60kg, 165cm, faccio palestra 3 volte a settimana e voglio aumentare massa muscolare"}'

🔐 __Sicurezza e Privacy__

Nessun dato sensibile viene salvato in produzione

Possibilità di disabilitare il salvataggio delle conversazioni

API Key private caricate tramite .env

📈 __Sviluppi futuri__

🧬 Integrazione con profili sanitari e wearable

📊 Dashboard utente

🌍 Multilingua e localizzazione

🔐 Autenticazione e gestione utenti

🧑‍⚕️ Supervisione professionale opzionale

📄 __Licenza__

Questo progetto è distribuito sotto licenza MIT.

📬 __Contatti__

Per suggerimenti o segnalazioni, apri un’issue su GitHub:
https://github.com/BonomeMichele/NutriBot/issues

🧠 __Contribuisci anche tu al futuro dell’educazione alimentare!__
