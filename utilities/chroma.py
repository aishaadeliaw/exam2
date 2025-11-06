import streamlit as st
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

    api_key = st.session_state.get("openai_api_key")

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
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
def answer_query_with_rag(collection, query, report, csv, chat_history):
    
    try:
        # Retrieve relevant chunks
        results = query_chroma_collection(collection, query, n_results=3)
        
        if not results['documents'][0]:
            return "No relevant information found in the database.", []
        
        relevant_chunks = results['documents'][0]

        # Build context from relevant chunks
        context = "\n\n".join([
            f"[Chunk {i+1}]\n{chunk}" 
            for i, chunk in enumerate(relevant_chunks)
        ])

        # Generate answer using LLM
        with st.spinner("Generating answer..."):
            answer = openai.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {"role": "user",
                    "content": f"""Answer the following question based on the context provided.

                    Question: {query}
                    Report: {report}
                    CSV: {csv}
                    Document context: {context}
                    Chat history: {chat_history}

                    Answer only based on the context above. If the answer cannot be found in the context, say so.
                    Perform an internet search only if the user asks for it."""
                    }
                ]
            )

        response = answer.choices[0].message.content

        return response
    
    except Exception as e:
        st.error(f"Error answering query: {e}")