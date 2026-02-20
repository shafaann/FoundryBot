import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
# Ensure these imports are available in your environment
# from vector import startup_retriever, industry_retriever, consumer_retriever

# =========================
# 1. PAGE SETUP & THEME
# =========================
st.set_page_config(page_title="Startup AI Assistant", layout="wide", page_icon="🚀")

# Injection of Custom CSS for the Dark Neon UI
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0b071a;
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #120c2b !important;
        border-right: 1px solid #2d1b5e;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(28, 20, 51, 0.6);
        border: 1px solid #3d2b7a;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Containers / Cards */
    .custom-card {
        background: rgba(28, 20, 51, 0.5);
        border: 1px solid #3d2b7a;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    /* Chat Styling */
    .stChatMessage {
        background-color: #1c1433 !important;
        border: 1px solid #4a308c !important;
        border-radius: 15px !important;
        margin-bottom: 10px;
    }
    
    /* Titles and Accents */
    h1, h2, h3 {
        color: #c77dff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-thumb {
        background: #4a308c;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================
# 2. CORE LOGIC (RAG)
# =========================
@st.cache_resource
def get_chain():
    model = OllamaLLM(model="gemma3:1b")
    template = """
    You are a professional startup intelligence assistant.
    User Idea: {idea}
    Retrieved Data: {records}
    
    Provide a concise analysis:
    1. Survival Patterns
    2. Growth Signals
    3. Target Users
    4. Strategic Risks
    
    Tone: Analytical, high-tech, like a VC dashboard.
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt | model

# Initializing chain (Make sure Ollama is running)
try:
    chain = get_chain()
except Exception as e:
    st.error(f"Ollama Connection Error: {e}")

# =========================
# 3. SIDEBAR (History)
# =========================
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🚀 FoundryBOT</h2>", unsafe_allow_html=True)
    st.button("+ New Chat", use_container_width=True)
    
    st.markdown("### Chat History")
    history = ["AI Fitness App Idea", "Startups in India 2012", "Health Tech Trends", "Funding in NYC"]
    for item in history:
        st.button(f"💬 {item}", key=item, use_container_width=True, type="secondary")
    
    st.markdown("<br>" * 5, unsafe_allow_html=True) # This creates 5 lines of empty space
    st.button("⚙️ Settings", use_container_width=True)

# =========================
# 4. TOP DASHBOARD ROW
# =========================
st.markdown("### 📊 Intelligence & Analytics Dashboard")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Startups", "3,876", "+12%")
m2.metric("Success Rate", "67.8%", "📈")
m3.metric("Avg Funding", "$2.4M", "High")
m4.metric("Active VCs", "142", "Steady")

st.markdown("---")

# =========================
# 5. MAIN CONTENT (CHAT + ANALYTICS)
# =========================
left_col, right_col = st.columns([1.6, 1])

with left_col:
    st.markdown("#### 🤖 AI Startup Consultant")
    
    # Session state for chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat Container
    chat_box = st.container(height=500, border=False)
    for msg in st.session_state.messages:
        with chat_box.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input Logic
    if idea := st.chat_input("Ask about startups, ideas, markets..."):
        # User display
        st.session_state.messages.append({"role": "user", "content": idea})
        with chat_box.chat_message("user"):
            st.markdown(idea)

        # RAG Execution
        with chat_box.chat_message("assistant"):
            with st.spinner("Analyzing Market Data..."):
                # Placeholder for your retriever logic
                # startup_recs = startup_retriever.invoke(idea)
                # industry_recs = industry_retriever.invoke(idea)
                # combined_data = "\n".join([d.page_content for d in (startup_recs + industry_recs)])
                
                # Sample Response
                response = chain.invoke({"idea": idea, "records": "Market data suggests 15% growth."})
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()

with right_col:
    st.markdown("#### 📈 Startup Analytics")
    
    # Industry Pie Chart Placeholder
    with st.container():
        st.write("**Industry Distribution**")
        # Using built-in chart for simplicity
        st.bar_chart({"AI/ML": 28, "Health": 22, "Fintech": 18, "EdTech": 15})
        
    # Top Cities Table
    st.markdown("#### 📍 Top Cities")
    st.table({
        "City": ["Bangalore", "Delhi", "Mumbai", "Chennai"],
        "Count": [420, 389, 312, 276]
    })

    # Success Probability Gauge (Custom Styled)
    st.markdown("""
        <div style="background: rgba(157, 78, 221, 0.2); padding: 20px; border-radius: 15px; border: 1px solid #9d4edd; text-align: center;">
            <h5 style="margin:0;">Success Probability</h5>
            <h1 style="color: #c77dff; margin: 10px 0;">72%</h1>
            <p style="color: #00ff88; font-weight: bold;">Good Opportunity</p>
        </div>
    """, unsafe_allow_html=True)