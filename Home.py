import streamlit as st
from utilities.tab1 import app1

# Title
st.markdown('<h1 style="color: #06402b;">Ask Hukumi 2.0</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("About Ask Hukumi")
    st.text("""
    Ask Hukumi is a tool for you to ask questions regarding any legal document that you upload.
    'Hukum' means 'law' in Indonesian, and 'Hukumi' is just a play on the word :)
    Enjoy!
    """)
    st.subheader("Disclaimer:")
    st.text("""
    Ask Hukumi is provided for informational purposes only.
    It does not constitute legal advice or opinion and should not be relied upon as a substitute for professional consultation with a qualified attorney or legal advisor.
    """)

# Tabs
tab1, tab2 = st.tabs(["Compliance Report and CSV", "Compliance Review"])

with tab1:
    app1()
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)