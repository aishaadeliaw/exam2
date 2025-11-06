import streamlit as st
import openai
from utilities.tab1 import upload_document
from utilities.tab2 import report_csv
from utilities.tab3 import ai_chat

# Page config
st.set_page_config(
    page_title="Ask Hukumi 2.0 - Compliance Assistant",
    layout="wide"
)

# Check if API key is valid
def validate_api_key(openai_api_key):
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="test",
        )
        return True, "Valid API key"
    except openai.AuthenticationError:
        return False, "Invalid API key"
    except openai.RateLimitError:
        return False, "API key valid but rate limit exceeded"
    except Exception as e:
        return False, f"Error: {str(e)}"
        
# Ask user for API key
@st.dialog("API Key Input", dismissible=False)
def api_key_input():
    name = st.text_input("Name")
    openai_api_key = st.text_input("Your API key", type="password")
    
    if name and openai_api_key and st.button("Submit"):
        with st.spinner("Validating API key..."):

            is_valid, message = validate_api_key(openai_api_key)

            if is_valid:
                st.session_state.openai_api_key = openai_api_key
                st.session_state.name = name

                # Set it globally for OpenAI library
                openai.api_key = openai_api_key
                st.success(message)
                st.rerun()

            else:
                st.error(message)   

if "openai_api_key" not in st.session_state and "name" not in st.session_state:
    st.session_state.openai_api_key = None
    st.session_state.name = None
    api_key_input()
    
# Custom layout
st.markdown("""
<style>
    .stApp {
        background: #eef6f3;
    }
    
    .main-header {
        background: linear-gradient(90deg, #06402b 0%, #0a5c3d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-title {
        color: #b29700;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .subtitle {
        color: #ffffff;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    .feature-card {
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
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #b29700;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        color: #b29700;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .card-description {
        color: #666666;
        font-size: 1rem;
        line-height: 1.4;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(90deg, #06402b 0%, #0a5c3d 100%);
        border-radius: 10px;
        padding: 0.7rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1.5rem 2rem;
        font-weight: 600;
        border-radius: 30px;
        font-size: 3rem;
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: #b29700;
        color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #b7b7b7;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06402b 0%, #0a5c3d 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">Ask Hukumi 2.0</div>
    <div class="subtitle">Your AI-Powered Compliance Assistant</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if st.session_state.name:
        st.subheader(f"Hi, {st.session_state.name}!")
        
    st.markdown("---")
    
    st.markdown("### 💡 About Ask Hukumi 2.0")
    st.markdown("""
    Ask Hukumi 2.0 is a compliance assistant powered by GPT-5, aiming at making compliance work easier.
    
    '*Hukum*' means '*law*' in Indonesian.
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔑 Key Features")
    st.markdown("""
    - ✅ Multi-document upload
    - ✅ Obligation extraction
    - ✅ Tailor-made report and CSV
    - ✅ Smart citations
    - ✅ Downloadable output
    - ✅ Interactive chat
    """)
    
    st.markdown("---")
    
    st.markdown("##### Disclaimer")
    st.caption("""
    This assistant provides analysis for informational purposes only and does not constitute legal advice.
    Always consult qualified legal professionals.
    """)

# Feature cards
st.markdown(
    "<h4 style='color: #0b7851;'>Features</h4>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Compliance Report and CSV</div>
        <div class="card-description">
            Upload documents and generate comprehensive report and CSV with extracted obligations and pinpoint citations
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">💬</div>
        <div class="card-title">Ask Questions</div>
        <div class="card-description">
            Chat with AI to enquire about the report and CSV
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📥</div>
        <div class="card-title">Export Data</div>
        <div class="card-description">
            Download output in .docx and .csv format
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📄 Upload Documents", "📊 Compliance Report and CSV", "💬 Ask Questions"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    upload_document()

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    report_csv()

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    ai_chat()