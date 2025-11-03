import streamlit as st
import os
from utilities.chroma import answer_query_with_rag

def ai_chat():
    
    st.markdown('<h4 style="color: #0b7851;">Ask Questions</h4>', unsafe_allow_html=True)
    st.markdown("""You can ask questions regarding the documents you have uploaded in the first tab.
    Make sure you have generated the compliance report and CSV in the second tab.""")

    api_key = os.environ.get("OPENAI_API_KEY")

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
            if not st.session_state.collection or not st.session_state.input_list or not st.session_state.report or not st.session_state.clean_csv:
                st.warning("Please upload documents and generate the compliance report and CSV first")
            
            else:
                response = answer_query_with_rag(
                    collection=st.session_state.collection,
                    query=prompt,
                    report=st.session_state.report,
                    csv=st.session_state.clean_csv,
                    input_list=st.session_state.input_list,
                    # n_results=3,
                    chat_history=st.session_state.messages
                )
                st.markdown(response)
        
                st.session_state.messages.append({"role": "assistant", "content": response})