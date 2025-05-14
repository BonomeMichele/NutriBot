🧠 NutriBot – Chatbot Nutrizionista con RAG
NutriBot è un assistente virtuale specializzato in nutrizione, in grado di generare diete personalizzate grazie alla tecnologia RAG (Retrieval-Augmented Generation) basata su fonti ufficiali italiane (LARN, INRAN, CREA).

🚀 Caratteristiche
🥗 Diete su misura in base al profilo utente

📚 Recupero intelligente di informazioni da documenti nutrizionali

💬 Interfaccia chat reattiva e moderna

🔊 Output vocale con ElevenLabs (opzionale)

📱 Ottimizzato per dispositivi mobili

🔍 Ricerca contestuale su domande nutrizionali

🛠️ Requisiti
Python 3.8+

FastAPI, Llama-Index

OpenAI API Key

ElevenLabs (opzionale)

⚙️ Installazione Rapida
bash
Copy
Edit
git clone https://github.com/BonomeMichele/NutriBot.git
cd NutriBot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Crea un file .env:

ini
Copy
Edit
OPENAI_API_KEY=sk-...
Aggiungi i documenti nutrizionali in app/static/documents/.

▶️ Avvio
bash
Copy
Edit
python run.py
# oppure in sviluppo
uvicorn app.main:app --reload
Visita http://localhost:8000.

🧭 Struttura Progetto
bash
Copy
Edit
NutriBot/
├── app/               # Codice applicazione
│   ├── api/           # Endpoints API
│   ├── core/          # Motori dietetici e RAG
│   ├── db/            # Accesso ai dati
│   ├── models/        # Modelli e schemi
│   ├── services/      # Logica di servizio
│   ├── static/        # Documenti e JS
│   └── templates/     # Frontend HTML
├── requirements.txt
├── run.py
└── .env
📡 API Principali
Metodo	Endpoint	Descrizione
POST	/api/chat/message	Invia messaggio al chatbot
POST	/api/diet/generate	Genera una dieta personalizzata
GET	/api/chat/history/{chat_id}	Cronologia chat
DELETE	/api/chat/{chat_id}	Elimina chat

Esempio:
bash
Copy
Edit
curl -X POST http://localhost:8000/api/diet/generate \
  -H "Content-Type: application/json" \
  -d '{"user_profile": "Uomo, 35 anni, 80kg, 178cm, sportivo. Obiettivo: perdere peso."}'
📌 Sviluppi Futuri
📱 App mobile integrata (Flutter/React Native)

📊 Dashboard con tracciamento progressi nutrizionali

🤝 Integrazione con dispositivi wearable (Fitbit, Apple Watch)

🗣️ Comprensione vocale diretta (Speech-to-Text)

🧾 Report PDF esportabili per piani alimentari

📄 Licenza
MIT

