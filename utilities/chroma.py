import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os
import openai
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

# RAG function
def answer_query_with_rag(collection, query, report, csv, input_list, chat_history):

    # # Retrieve relevant chunks
    # results = query_chroma_collection(collection, query, n_results)
    
    # if not results['documents'][0]:
    #     return "No relevant information found in the database.", []
    
    # relevant_chunks = results['documents'][0]

    # # Build context from relevant chunks
    # context = "\n\n".join([
    #     f"[Chunk {i+1}]\n{chunk}" 
    #     for i, chunk in enumerate(relevant_chunks)
    # ])

    # Generate answer using LLM
    answer = openai.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "user",
            "content": f"""Answer the following question based on the context provided.

            Question: {query}
            Report: {report}
            CSV: {csv}
            Input list: {input_list}
            Chat history: {chat_history}

            Answer only based on the context above. If the answer cannot be found in the context, say so."""
            }
        ]
    )

    response = answer.choices[0].message.content

    return response