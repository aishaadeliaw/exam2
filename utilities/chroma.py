import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import uuid
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

    print("\n>> COLLECTION INITIALISED\n")

    return collection

# Store chunks
def store_chunks_in_chroma_collection(collection, document_name, document_chunk, document_id):

    guid = uuid.uuid4()

    guid_string = str(guid)

    collection.add(
        documents=[document_chunk],
        metadatas=[{"document_name": document_name}],
        ids=[document_id]
    )

# Query
def query_chroma_collection(collection, query, n_results):

    documents = collection.query(
        query_texts=[query],
        include=["documents", "metadatas"],
        n_results=n_results
    )

    return documents