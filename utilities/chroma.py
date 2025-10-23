import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

# Setup Chroma
def create_chroma_collection(collection_name):

    os.makedirs(f"./data/chromadb/{collection_name}", exist_ok=True)

    chroma_client = chromadb.PersistentClient(f"./data/chromadb/{collection_name}")

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        ),
        metadata={"hnsw:space": "cosine"}
    )

    return collection

# Store chunks
def store_chunks_in_chroma_collection(collection, document_name, document_chunk, document_id):

    collection.add(
        metadatas=[{
            "document": document_name,
            "chunk_id": document_id
        }],
        documents=[document_chunk],
        ids=[document_id]
    )
    
# Query
def query_chroma_collection(collection, query, n_results=3):

    documents = collection.query(
        query_texts=[query],
        include=["documents", "metadatas"],
        n_results=n_results
    )

    return documents