import streamlit as st
import os
import PyPDF2
from utilities.chroma import create_chroma_collection, store_chunks_in_chroma_collection
from utilities.chunk import chunk_by_sentences

def upload_document():

    # Session states
    if "collection" not in st.session_state:
        st.session_state.collection = None
    
    if "collection_name" not in st.session_state:
        st.session_state.collection_name = None

    if "chunks" not in st.session_state:
        st.session_state.chunks = None

    if "uploaded_documents" not in st.session_state:
        st.session_state.uploaded_documents = None

    # Upload documents
    st.markdown('<h4 style="color: #0b7851;">Upload Documents</h4>', unsafe_allow_html=True)

    uploaded_documents = st.file_uploader("Choose PDF files to upload", type=["pdf"], accept_multiple_files=True)

    if not uploaded_documents:
        st.session_state.collection = None
        st.session_state.collection_name = None
        st.session_state.chunks = None

    # Create Chroma collection
    collection_name = st.text_input("What is the name of your collection?")

    if uploaded_documents and collection_name and st.button("Upload and Create Collection"):
        collection = create_chroma_collection(f"{collection_name}")
        st.session_state.collection = collection
        st.session_state.collection_name = collection_name

        # Store documents
        with st.spinner("Uploading and processing documents..."):

            document_folder = "document_folder"

            if not os.path.exists(document_folder):
                os.makedirs(document_folder)

            all_chunks = {}

            for uploaded_document in uploaded_documents:
                file_name = uploaded_document.name
                file_path = os.path.join(document_folder, file_name)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_document.getbuffer())
                
                st.success(f"PDF file '{file_name}' has been uploaded successfully")

                # Read documents
                try:
                    with open(file_path, "rb") as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        num_pages = len(pdf_reader.pages)
                        text = ""
                
                        for page in range(num_pages):
                            text += pdf_reader.pages[page].extract_text() + "\n\n"

                    # Chunk documents
                    chunks = chunk_by_sentences(text)

                    # Store chunks in Chroma
                    for idx, chunk in enumerate(chunks):
                        doc_id = f"{file_name}: {idx}"

                        store_chunks_in_chroma_collection(
                            collection=st.session_state.collection,
                            document_name=file_name,
                            document_chunk=chunk['content'],
                            document_id=doc_id
                        )

                    all_chunks[file_name] = [
                        {"idx": idx, "chunk": chunk} for idx, chunk in enumerate(chunks)
                    ]

                    st.info(f"Created and stored {len(chunks)} chunks from '{file_name}'")

                except Exception as e:
                    st.error(f"Error processing '{file_name}': {e}")
            
            st.session_state.chunks = all_chunks
            st.session_state.uploaded_documents = uploaded_documents

    # Show chunks
    if st.session_state.chunks:
        for file_name, chunks in st.session_state.chunks.items():
            with st.expander(f"Document Chunks from '{file_name}' ({len(chunks)} chunks)"):
                for item in chunks:
                    idx = item["idx"]
                    chunk = item["chunk"]
                    with st.expander(f"Chunk {idx} – {chunk['header']}"):
                        st.write(chunk["content"])