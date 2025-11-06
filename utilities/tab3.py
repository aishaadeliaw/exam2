import streamlit as st
import os
from utilities.chroma import answer_query_with_rag

def ai_chat():
    
    st.markdown('<h4 style="color: #0b7851;">Ask Questions</h4>', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        .description-card {
            background: #ffffff;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
            border: 2px solid transparent;
            margin-bottom: 1rem;
        }
        
        .card-description {
            color: #666666;
            font-size: 1rem;
            line-height: 1.4;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="description-card">
        <div class="card-description">
            You can ask questions about the documents and output.
            Please make sure you have generated the report and CSV.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What is your question?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not st.session_state.collection or not st.session_state.report or not st.session_state.clean_csv:
                st.warning("Please upload documents and generate the report and CSV first")
            
            else:
                response = answer_query_with_rag(
                    collection=st.session_state.collection,
                    query=prompt,
                    report=st.session_state.report,
                    csv=st.session_state.clean_csv,
                    chat_history=st.session_state.messages
                )
                st.markdown(response)
        
                st.session_state.messages.append({"role": "assistant", "content": response})