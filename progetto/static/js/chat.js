// Gestione delle chat e interazione con l'API
document.addEventListener('DOMContentLoaded', function() {
    // Elementi DOM
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatContainer = document.getElementById('chatContainer');
    const newChatBtn = document.getElementById('newChatBtn');
    const chatList = document.getElementById('chatList');
    const noChatsMsg = document.getElementById('noChatsMsg');
    const deleteAllBtn = document.getElementById('deleteAllBtn');
    const currentChatTitle = document.getElementById('currentChatTitle');
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const voiceOutputBtn = document.getElementById('voiceOutputBtn');

    // Stato dell'applicazione
    let currentChatId = null;
    let isProcessing = false;
    let voiceOutputEnabled = false;

    // Inizializzazione
    initializeApp();

    // Funzione di inizializzazione
    function initializeApp() {
        // Carica le chat esistenti
        fetchChats();
        
        // Inizializza una nuova chat se non ce ne sono
        if (!currentChatId) {
            startNewChat();
        }

        // Event listeners
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keydown', handleInputKeydown);
        chatInput.addEventListener('input', adjustInputHeight);
        newChatBtn.addEventListener('click', startNewChat);
        deleteAllBtn.addEventListener('click', deleteAllChats);
        menuToggle.addEventListener('click', toggleSidebar);
        voiceOutputBtn.addEventListener('click', toggleVoiceOutput);

        // Aggiusta l'altezza dell'input
        adjustInputHeight();
    }

    // Aggiusta l'altezza dell'input in base al contenuto
    function adjustInputHeight() {
        chatInput.style.height = 'auto';
        chatInput.style.height = (chatInput.scrollHeight) + 'px';
        sendBtn.disabled = chatInput.value.trim() === '';
    }

    // Gestione del tasto Invio nell'input
    function handleInputKeydown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    // Invia un messaggio
    async function sendMessage() {
        if (isProcessing || chatInput.value.trim() === '') return;

        const message = chatInput.value.trim();
        chatInput.value = '';
        chatInput.style.height = 'auto';
        sendBtn.disabled = true;
        isProcessing = true;

        // Aggiunge il messaggio dell'utente alla chat
        appendMessage(message, 'user');

        // Mostra l'indicatore di caricamento
        const loadingElement = showLoading();

        try {
            // Invia il messaggio all'API
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chat_id: currentChatId,
                    message: message,
                    timestamp: new Date().toISOString()
                }),
            });

            const data = await response.json();
            
            // Rimuovi l'indicatore di caricamento
            chatContainer.removeChild(loadingElement);

            // Aggiorna l'ID della chat se necessario
            if (data.chat_id && !currentChatId) {
                currentChatId = data.chat_id;
                updateURLWithChatId();
            }

            // Aggiungi la risposta del bot alla chat
            appendMessage(data.message, 'assistant', data.sources);

            // Se è l'output vocale è abilitato, leggi la risposta
            if (voiceOutputEnabled) {
                playVoiceResponse(data.message);
            }

            // Aggiorna la lista delle chat
            fetchChats();
        } catch (error) {
            console.error('Errore:', error);
            // Rimuovi l'indicatore di caricamento
            chatContainer.removeChild(loadingElement);
            // Mostra un messaggio di errore
            appendMessage('Mi dispiace, si è verificato un errore nella comunicazione con il server.', 'assistant');
        }

        isProcessing = false;
    }

    // Aggiungi un messaggio alla chat
    function appendMessage(message, role, sources = []) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `message-container ${role === 'user' ? 'user-container' : 'assistant-container'}`;

        const avatar = document.createElement('div');
        avatar.className = `avatar ${role === 'user' ? 'avatar-user' : 'avatar-assistant'}`;
        avatar.innerHTML = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-leaf"></i>';
        messageContainer.appendChild(avatar);

        const messageElement = document.createElement('div');
        messageElement.className = `message ${role === 'user' ? 'user-message' : 'assistant-message'}`;
        
        // Formattiamo il messaggio con markdown se è del bot
        if (role === 'assistant') {
            // Sostituisce i caratteri ** con <strong> e </strong>
            let formattedMessage = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            // Sostituisce le linee con elenchi puntati
            formattedMessage = formattedMessage.replace(/^- (.*?)$/gm, '<li>$1</li>');
            formattedMessage = formattedMessage.replace(/<li>(.*?)<\/li>/g, function(match) {
                return '<ul>' + match + '</ul>';
            });
            // Sostituisce i tag <ul><ul> con un singolo <ul>
            formattedMessage = formattedMessage.replace(/<\/ul>\s*<ul>/g, '');
            // Sostituisce le linee vuote con paragrafi
            formattedMessage = formattedMessage.replace(/\n\n/g, '</p><p>');
            // Avvolge il testo in paragrafi
            formattedMessage = '<p>' + formattedMessage + '</p>';
            
            messageElement.innerHTML = formattedMessage;
        } else {
            messageElement.textContent = message;
        }
        
        // Aggiungi l'ora del messaggio
        const timeElement = document.createElement('div');
        timeElement.className = 'message-time';
        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageElement.appendChild(timeElement);

        // Aggiungi le fonti se presenti
        if (sources && sources.length > 0) {
            const sourcesElement = document.createElement('div');
            sourcesElement.className = 'message-sources';
            sourcesElement.textContent = 'Fonti: ' + sources.join(', ');
            messageElement.appendChild(sourcesElement);
        }

        messageContainer.appendChild(messageElement);
        chatContainer.appendChild(messageContainer);

        // Scorri alla fine della chat
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Mostra l'indicatore di caricamento
    function showLoading() {
        const loadingElement = document.createElement('div');
        loadingElement.className = 'loading';
        loadingElement.innerHTML = `
            <div class="loading-text">Il nutrizionista sta elaborando...</div>
            <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        chatContainer.appendChild(loadingElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return loadingElement;
    }

    // Inizia una nuova chat
    function startNewChat() {
        currentChatId = null;
        currentChatTitle.textContent = 'Nuova Chat';
        chatContainer.innerHTML = `
            <div class="welcome-message">
                <h2>Benvenuto al Chatbot Nutrizionista!</h2>
                <p>Puoi chiedermi informazioni su alimentazione e nutrizione, oppure richiedermi una dieta personalizzata fornendomi informazioni come età, sesso, peso, altezza, livello di attività fisica e obiettivi.</p>
                <p>Esempio: "Sono un uomo di 35 anni, peso 80kg, sono alto 178cm e faccio attività fisica 3 volte a settimana. Vorrei una dieta per perdere peso."</p>
            </div>
        `;
        updateURLWithChatId();
        
        // Chiudi la sidebar su mobile dopo aver selezionato una nuova chat
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('show');
        }
    }

    // Carica le chat esistenti
    async function fetchChats() {
        try {
            const response = await fetch('/api/chat/list');
            const data = await response.json();
            
            // Aggiorna la lista delle chat
            renderChatList(data.chats);
        } catch (error) {
            console.error('Errore nel caricamento delle chat:', error);
        }
    }

    // Renderizza la lista delle chat
    function renderChatList(chats) {
        chatList.innerHTML = '';
        
        if (chats.length === 0) {
            noChatsMsg.style.display = 'block';
            return;
        }
        
        noChatsMsg.style.display = 'none';
        
        chats.forEach(chat => {
            const chatItem = document.createElement('div');
            chatItem.className = `chat-item ${chat.id === currentChatId ? 'active' : ''}`;
            chatItem.innerHTML = `
                <span class="chat-title">${chat.title}</span>
                <button class="delete-chat" data-chat-id="${chat.id}">
                    <i class="fa-solid fa-trash"></i>
                </button>
            `;
            
            // Evento click sulla chat
            chatItem.addEventListener('click', () => loadChat(chat.id));
            
            // Evento click sul pulsante di eliminazione
            chatItem.querySelector('.delete-chat').addEventListener('click', (e) => {
                e.stopPropagation();
                deleteChat(chat.id);
            });
            
            chatList.appendChild(chatItem);
        });
    }

    // Carica una chat esistente
    async function loadChat(chatId) {
        if (isProcessing) return;
        
        currentChatId = chatId;
        isProcessing = true;
        
        // Svuota il container della chat
        chatContainer.innerHTML = '';
        
        try {
            // Ottieni lo storico della chat
            const response = await fetch(`/api/chat/history/${chatId}`);
            const history = await response.json();
            
            // Trova la chat nella lista per impostare il titolo
            const chatResponse = await fetch('/api/chat/list');
            const chatData = await chatResponse.json();
            const chat = chatData.chats.find(c => c.id === chatId);
            
            if (chat) {
                currentChatTitle.textContent = chat.title;
            }
            
            // Renderizza i messaggi
            history.forEach(msg => {
                appendMessage(msg.content, msg.role);
            });
            
            // Aggiorna l'URL
            updateURLWithChatId();
            
            // Chiudi la sidebar su mobile dopo aver selezionato una chat
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('show');
            }
        } catch (error) {
            console.error('Errore nel caricamento della chat:', error);
            appendMessage('Si è verificato un errore nel caricamento della chat.', 'assistant');
        }
        
        isProcessing = false;
    }

    // Elimina una chat
    async function deleteChat(chatId) {
        if (isProcessing) return;
        
        try {
            await fetch(`/api/chat/${chatId}`, {
                method: 'DELETE'
            });
            
            // Se la chat corrente è stata eliminata, iniziane una nuova
            if (chatId === currentChatId) {
                startNewChat();
            }
            
            // Aggiorna la lista delle chat
            fetchChats();
        } catch (error) {
            console.error('Errore nell\'eliminazione della chat:', error);
        }
    }

    // Elimina tutte le chat
    async function deleteAllChats() {
        if (isProcessing) return;
        
        if (!confirm('Sei sicuro di voler eliminare tutte le chat?')) {
            return;
        }
        
        try {
            await fetch('/api/chat/', {
                method: 'DELETE'
            });
            
            // Inizia una nuova chat
            startNewChat();
            
            // Aggiorna la lista delle chat
            fetchChats();
        } catch (error) {
            console.error('Errore nell\'eliminazione di tutte le chat:', error);
        }
    }

    // Aggiorna l'URL con l'ID della chat
    function updateURLWithChatId() {
        const url = new URL(window.location);
        if (currentChatId) {
            url.searchParams.set('chat_id', currentChatId);
        } else {
            url.searchParams.delete('chat_id');
        }
        window.history.replaceState({}, '', url);
    }

    // Apri/chiudi la sidebar su mobile
    function toggleSidebar() {
        sidebar.classList.toggle('show');
    }

    // Attiva/disattiva l'output vocale
    function toggleVoiceOutput() {
        voiceOutputEnabled = !voiceOutputEnabled;
        voiceOutputBtn.classList.toggle('active', voiceOutputEnabled);
        
        // Mostra lo stato dell'output vocale
        const voiceStatus = document.createElement('div');
        voiceStatus.className = 'voice-status show';
        voiceStatus.innerHTML = `
            <span class="pulse"></span>
            Output vocale ${voiceOutputEnabled ? 'attivato' : 'disattivato'}
        `;
        
        document.body.appendChild(voiceStatus);
        
        // Rimuovi lo stato dopo 2 secondi
        setTimeout(() => {
            document.body.removeChild(voiceStatus);
        }, 2000);
        
        // Controlla se il widget ElevenLabs è stato caricato
        const elevenLabsWidget = document.querySelector('elevenlabs-convai');
        if (voiceOutputEnabled && elevenLabsWidget) {
            // Posizione corretta per il widget
            elevenLabsWidget.style.position = 'fixed';
            elevenLabsWidget.style.top = '20px';
            elevenLabsWidget.style.right = '20px';
            elevenLabsWidget.style.zIndex = '9999';
        }
    }

    // Riproduzione vocale della risposta
    function playVoiceResponse(text) {
        // Controlla se il widget ElevenLabs è stato caricato
        const elevenLabsWidget = document.querySelector('elevenlabs-convai');
        if (elevenLabsWidget && typeof elevenLabsWidget.say === 'function') {
            // Limita il testo per evitare problemi con testi lunghi
            const maxTextLength = 500;
            const truncatedText = text.length > maxTextLength ? 
                text.substring(0, maxTextLength) + '...' : text;
            
            // Rimuovi i markdown per la lettura vocale
            const cleanText = truncatedText
                .replace(/\*\*(.*?)\*\*/g, '$1')
                .replace(/^- (.*?)$/gm, '$1');
            
            // Leggi il testo
            elevenLabsWidget.say(cleanText);
        }
    }

    // Verifica se è presente un chat_id nell'URL
    function checkUrlForChatId() {
        const urlParams = new URLSearchParams(window.location.search);
        const chatIdParam = urlParams.get('chat_id');
        
        if (chatIdParam) {
            loadChat(chatIdParam);
        }
    }

    // Verifica l'URL per un chat_id dopo aver caricato le chat
    setTimeout(checkUrlForChatId, 500);
});
