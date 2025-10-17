import streamlit as st
import os
import openai
import PyPDF2
from dotenv import load_dotenv
from utilities.chroma import create_chroma_collection, store_chunks_in_chroma_collection
from utilities.llm_agent import agent_with_search

load_dotenv()

if "investigation_collection" not in st.session_state:
    st.session_state.investigation_collection = None

# Title
st.title("Ask Hukumi 2.0")

# Upload document
st.subheader("Upload Documents")
uploaded_documents = st.file_uploader("Choose a PDF file to upload", type=["pdf"], accept_multiple_files=True)

collection_name = st.text_input("What is the name of your collection?")

if collection_name:
    investigation_collection = create_chroma_collection(f"{collection_name}")
    st.session_state.investigation_collection = investigation_collection

if uploaded_documents and st.button("Upload"):
    with st.spinner("Uploading document..."):

        document_folder = "document_folder"

        if not os.path.exists(document_folder):
            os.makedirs(document_folder)

        for uploaded_document in uploaded_documents:
            file_name = uploaded_document.name
            file_path = os.path.join(document_folder, file_name)
              
            with open(file_path, "wb") as f:
                f.write(uploaded_document.getbuffer())
                
            st.success(f"PDF file '{file_name}' has been uploaded successfully")

            try:
                with open(file_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    num_pages = len(pdf_reader.pages)
                    text = ""
            
                    for page in range(num_pages):
                        text += pdf_reader.pages[page].extract_text() + "\n\n"
        
                # Chunk document
                chunk_size = 5000
                chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

                st.write(chunks)

                # Add chunks to Chroma
                for idx, chunk in enumerate(chunks):
                    doc_id = f"{file_name}::{idx}"  # unique across folders
                    st.write(f"Trying to add doc_id: {doc_id}")
                    store_chunks_in_chroma_collection(
                        collection=st.session_state.investigation_collection,
                        document_name=file_name,
                        document_chunk=chunk,
                        document_id=doc_id
                    )
                    # Optional: if your add function supports metadata dicts, you could extend it to accept:
                    # metadatas=[{"document_name": document_name, "source_folder": folder_path, "source_path": doc_path}]
                    st.write("Success")

                st.success(f"Added {len(chunks)} chunks from {file_name} to ChromaDB.")

            except Exception as e:
                st.error(f"Error processing {file_name}: {e}")

# Agent
user_objective = st.text_input("What is your objective?")
if user_objective and st.button("Run Agent"):

    agent_still_searching = True

    input_list = [
        {"role": "user", "content": user_objective}
    ]

    number_of_loops = 0

    while agent_still_searching == True:

        st.write(f"Loop Number: {number_of_loops}")

        number_of_loops = number_of_loops + 1

        input_list = agent_with_search(st.session_state.investigation_collection, user_objective, input_list)

        #st.write(input_list)

        if number_of_loops == 2:
            agent_still_searching = False

        response = openai.responses.create(
            model="gpt-5-mini",
            instructions=(
                f"""Your objective is: {user_objective}.
                You have retrieved document chunks from ChromaDB searches.
                Find all compliance checklist relevant to the objective and make a report.
                For your report, you must summarise, cite, and reference the actual content of these document chunks.
                Include direct quotes or paraphrased information from the documents where relevant.
                Make it clear which information comes from which document."""
            ),
            input=input_list
        )

        report = response.output_text

        st.write(report)