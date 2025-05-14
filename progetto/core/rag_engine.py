from typing import List, Dict, Any, Optional
import logging
import os
from pathlib import Path

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
    set_global_service_context
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from app.config import settings

# Configurazione logging
logger = logging.getLogger(__name__)

# Variabili globali per il motore RAG
_vector_index = None

def initialize_rag_engine() -> None:
    """
    Inizializza il motore RAG caricando i documenti e creando gli embeddings.
    Se esiste già un indice precedentemente salvato, lo carica invece di ricrearlo.
    """
    global _vector_index
    
    # Verifica che la chiave API OpenAI sia impostata
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY non trovata nelle variabili d'ambiente")
    
    # Imposta il contesto del servizio Llama-Index
    llm = OpenAI(model=settings.CHAT_MODEL, api_key=settings.OPENAI_API_KEY)
    embed_model = OpenAIEmbedding(model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
    )
    set_global_service_context(service_context)
    
    # Percorso del vectorstore
    storage_path = settings.VECTORSTORE_PATH
    
    # Se esiste già un indice salvato, caricalo
    if os.path.exists(storage_path) and any(os.listdir(storage_path)):
        logger.info(f"Caricamento dell'indice esistente dalla directory {storage_path}")
        try:
            storage_context = StorageContext.from_defaults(persist_dir=str(storage_path))
            _vector_index = load_index_from_storage(storage_context)
            logger.info("Indice caricato con successo")
        except Exception as e:
            logger.error(f"Errore nel caricamento dell'indice: {e}")
            logger.info("Creazione di un nuovo indice...")
            _create_new_index(storage_path)
    else:
        # Altrimenti, crea un nuovo indice
        logger.info("Nessun indice esistente trovato. Creazione di un nuovo indice...")
        _create_new_index(storage_path)
    
    logger.info("Motore RAG inizializzato correttamente")

def _create_new_index(storage_path: Path) -> None:
    """
    Crea un nuovo indice di embeddings dai documenti e lo salva
    
    Args:
        storage_path: Percorso dove salvare l'indice
    """
    global _vector_index
    
    # Verifica che la directory dei documenti esista
    documents_dir = settings.DOCUMENTS_DIR
    if not os.path.exists(documents_dir):
        logger.warning(f"La directory dei documenti {documents_dir} non esiste. Creazione...")
        os.makedirs(documents_dir, exist_ok=True)
    
    # Verifica che ci siano documenti da caricare
    documents = list(documents_dir.glob("*.pdf")) + list(documents_dir.glob("*.docx")) + list(documents_dir.glob("*.txt"))
    if not documents:
        logger.warning(f"Nessun documento trovato in {documents_dir}. Scarica documenti nutrizionali prima di utilizzare il RAG.")
        # Creazione di un indice vuoto che può essere aggiornato in seguito
        _vector_index = VectorStoreIndex([])
        return
    
    # Carica i documenti dalla directory
    logger.info(f"Caricamento documenti da {documents_dir}")
    try:
        documents = SimpleDirectoryReader(str(documents_dir)).load_data()
        logger.info(f"Caricati {len(documents)} documenti")
        
        # Crea l'indice vettoriale
        _vector_index = VectorStoreIndex.from_documents(documents)
        
        # Salva l'indice per uso futuro
        _vector_index.storage_context.persist(persist_dir=str(storage_path))
        logger.info(f"Indice creato e salvato in {storage_path}")
    except Exception as e:
        logger.error(f"Errore durante la creazione dell'indice: {e}")
        raise

def query_rag(query: str, top_k: int = settings.TOP_K_RESULTS) -> Dict[str, Any]:
    """
    Interroga il motore RAG con una query utente
    
    Args:
        query: La query dell'utente
        top_k: Numero di risultati più rilevanti da recuperare
        
    Returns:
        Un dizionario con i risultati e il contesto recuperato
    """
    global _vector_index
    
    if _vector_index is None:
        logger.error("Il motore RAG non è stato inizializzato")
        raise RuntimeError("Il motore RAG non è stato inizializzato. Chiamare initialize_rag_engine() prima dell'uso")
    
    try:
        # Crea un query engine con il contesto
        query_engine = _vector_index.as_query_engine(
            similarity_top_k=top_k,
            response_mode="no_text"  # Restituisce solo i nodi rilevanti, non una risposta generata
        )
        
        # Esegui la query
        response = query_engine.query(query)
        
        # Estrai i nodi di contesto
        context_nodes = response.source_nodes
        
        # Estrai il testo da ogni nodo
        context_texts = [node.node.text for node in context_nodes]
        context_combined = "\n\n".join(context_texts)
        
        # Restituisci un dizionario con i risultati
        return {
            "query": query,
            "context": context_combined,
            "source_nodes": context_nodes,
            "num_results": len(context_nodes)
        }
    except Exception as e:
        logger.error(f"Errore durante la query al motore RAG: {e}")
        raise
