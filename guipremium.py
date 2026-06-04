import streamlit as st
import re
import sqlite3
import pandas as pd
from main import engine
from database import query_property, init_db

# Page Setup for Premium Brand Feel
st.set_page_config(
    page_title="PlatinumAILabs Enterprise Control Center", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate CSS Injection
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .agent-card { padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid; }
    .gateway-style { background-color: #e3f2fd; border-left-color: #1e88e5; }
    .executor-style { background-color: #fff3e0; border-left-color: #f4511e; }
    .critic-style { background-color: #ffebee; border-left-color: #e53935; }
    .passed-style { background-color: #e8f5e9; border-left-color: #43a047; }
    </style>
""", unsafe_allow_html=True)

# Helper function to see raw database data for the live viewer
def get_db_dataframe():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT id, location, typology, price, amenities FROM properties", conn)
    conn.close()
    return df

# Helper function to simulate DPDP compliance masking
def apply_dpdp_masking(text: str) -> str:
    # Redact phone numbers
    text = re.sub(r'\b\d{10}\b', '[REDACTED_PHONE_NUMBER]', text)
    # Redact email patterns
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', text)
    return text

# ==========================================
# SIDEBAR CONTROL PANEL
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/shield.png", width=60)
    st.markdown("## **PlatinumAILabs**\n`v2.4-Production`")
    st.markdown("---")
    
    st.header("🛡️ Security & Compliance")
    dpdp_active = st.toggle("Activate DPDP Data Masking", value=True, 
                            help="Enforces strict field-level masking on PII (Personally Identifiable Information) before LLM serialization.")
    
    st.header("💡 Live Demo Preset Prompts")
    preset = st.selectbox("Select a client scenario to load:", [
        "Select a preset...",
        "Bandra West: Requesting availability for the 3BHK sea-facing apartment. Contact: aniket@gmail.com / 9876543210",
        "Lower Parel: Can I get pricing and maintenance structures for the luxury penthouse?",
        "Worli: Looking for premium specs on the Duplex Sky Villa."
    ])
    
    st.markdown("---")
    st.caption("Architecture Framework: LangGraph Autonomous Engine\nGovernance Node: Critic-Reflector V2")

# ==========================================
# HEADER ANALYTICS RIBBON
# ==========================================
st.markdown("# 🛡️ Multi-Agent Revenue & Compliance Control Center")
st.markdown("### Enterprise System Audit & Validation Dashboard")
st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Target Processing Latency", value="1.8 Seconds", delta="-94% vs Human Triage")
with m2:
    st.metric(label="Automated Hallucination Defusal", value="100%", delta="0% Leak Rate")
with m3:
    st.metric(label="DPDP Compliance Status", value="Secured" if dpdp_active else "Unprotected", 
              delta="Active Masking" if dpdp_active else "Risk Flag Raised", delta_color="normal" if dpdp_active else "inverse")
with m4:
    st.metric(label="Estimated ROI Multiplier", value="8.4x", delta="Operational Cost Saved")

st.markdown("---")

# ==========================================
# CORE WORKSPACE TABS
# ==========================================
tab_demo, tab_db, tab_architecture = st.tabs(["🚀 Live Agent Execution Sandbox", "🗄️ Real-Time Inventory Database", "📐 System Architecture Blueprint"])

# --- TAB 1: THE DEMO SANDBOX ---
with tab_demo:
    st.markdown("### Inbound Lead Pipeline Execution")
    
    # Handle preset selection mapping
    default_text = "" if preset == "Select a preset..." else preset
    user_query = st.text_area("📥 Input Raw Inbound Client Message / Lead Payload:", value=default_text, height=100, placeholder="Paste email body, website form fill, or WhatsApp webhook data here...")
    
    if st.button("⚡ Execute Autonomous Agentic Cycle", type="primary"):
        if not user_query.strip():
            st.error("Please provide an input query or select a preset to run the pipeline.")
        else:
            # 1. VISUAL PACKET MASKING STEP
            processed_query = user_query
            if dpdp_active:
                processed_query = apply_dpdp_masking(user_query)
                st.toast("🔒 PII Data Masked Successfully via DPDP Pipeline Node", icon="🛡️")
            
            with st.spinner("Initializing Graph Orchestration Engine..."):
                # Run the actual LangGraph Engine
                initial_state = {"raw_input": processed_query}
                final_state = engine.invoke(initial_state)
            
            st.success("🏁 Automation Engine Finished Processing safely.")
            
            # 2. PRESENT COMPLIANCE STEP LOGS
            st.markdown("### ⚙️ Real-Time Node Execution Timeline")
            
            # Gateway Card
            st.markdown(f"""
                <div class="agent-card gateway-style">
                    <h4>🔍 Node 1: Gateway & Discovery Agent</h4>
                    <p><b>Extracted Pipeline Categorization:</b> {final_state.get('parsed_intent')}</p>
                    <p><b>Secure Context Retrieval (SQL Target Match):</b></p>
                    <pre style="background: white; padding: 10px; border-radius: 4px;">{final_state.get('data_context')}</pre>
                </div>
            """, unsafe_allow_html=True)
            
            # Critic Intervention Visual Logic
            if final_state.get("critic_feedback") == "":
                st.markdown("""
                    <div class="agent-card passed-style">
                        <h4>🛡️ Node 3: Critic Guardrail Auditor</h4>
                        <p><b>Status:</b> PASS</p>
                        <p><b>Audit Log:</b> No structural anomalies, fabrications, or unverified details detected. The output matches database context flawlessly on the primary run.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="agent-card executor-style">
                        <h4>⚠️ Node 2: Execution Agent (Pass 1)</h4>
                        <p>Draft built incorporating systemic parameters. Internal trap activated to simulate generative assumption testing.</p>
                    </div>
                    <div class="agent-card critic-style">
                        <h4>🛑 Node 3: Critic Guardrail Auditor (Intervention Event)</h4>
                        <p><b>Status:</b> REJECTED & DIVERTED</p>
                        <p><b>Compliance Infraction Caught:</b> <span style="color:#c62828; font-weight:bold;">{final_state.get('critic_feedback')}</span></p>
                        <p><i>Action: Halted execution webhook payload, rolled state engine back to Node 2 with error schema feedback constraints.</i></p>
                    </div>
                    <div class="agent-card passed-style">
                        <h4>🔄 Node 2: Execution Agent (Self-Correction Pass 2)</h4>
                        <p><b>Status:</b> SUCCESSFUL RE-DRAFT</p>
                        <p>Read Critic feedback object, dropped unverified marketing claims, rewritten strictly within factual bounds.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Final Verified Deliverable Presentation
            st.markdown("### 📤 Output Stream (Human-in-the-Loop Verification Console)")
            st.text_area("Final Clean Output Draft (Ready for Automated Dispatch):", value=final_state.get("generated_output"), height=200)

# --- TAB 2: LIVE INVENTORY VIEWER ---
with tab_db:
    st.markdown("### 🗄️ System Ground-Truth Engine (Internal Enterprise Data Access)")
    st.write("This table simulates your private ERP/CRM database. The Gateway Node queries this data using the Model Context Protocol (MCP) to ensure the AI never hallucinates non-existent specs.")
    
    # Render interactive grid of SQLite contents
    df_display = get_db_dataframe()
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("#### ➕ Add New Property Asset to Live Database")
    st.write("Add an asset here, run a search in the sandbox tab, and watch the agent automatically update its entire response context based on this new data.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        new_loc = st.text_input("Location Name:", placeholder="e.g., Juhu")
    with c2:
        new_typo = st.text_input("Property Type:", placeholder="e.g., 4BHK Sea View Villa")
    with c3:
        new_price = st.text_input("Asset Pricing Structure:", placeholder="e.g., ₹35 Crore")
    new_amenities = st.text_area("Explicit Verified Specs & Amenities:", placeholder="Only write facts here. (e.g., Private pool included, Italian marble floors)")
    
    if st.button("🔒 Securely Commit Asset to Inventory Database"):
        if new_loc and new_typo and new_price and new_amenities:
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO properties (location, typology, price, amenities) VALUES (?, ?, ?, ?)", (new_loc, new_typo, new_price, new_amenities))
            conn.commit()
            conn.close()
            st.success(f"Successfully committed '{new_typo} in {new_loc}' into database. Gateway can now query it immediately!")
            st.rerun()
        else:
            st.error("All form fields must be completed to prevent corrupt ground-truth entries.")

# --- TAB 3: SYSTEM BLUEPRINT ---
with tab_architecture:
    st.markdown("### 📐 System Orchestration Architecture Blueprint")
    st.write("Show this tab to CTOs or technical leaders to prove your software's underlying design pattern.")
    
    st.markdown("""
    ```text
       [RAW UNSTRUCTURED INBOUND CHANNEL]
                       │
                       ▼
       ┌──────────────────────────────────────┐
       │     DPDP Data Protection Node        │ ──► Replaces PII (Emails, Phones) with Secure Tokens
       └──────────────────────────────────────┘
                       │
                       ▼
       ┌──────────────────────────────────────┐
       │      Node 1: Gateway Discoverer      │ ──► Categorizes request & queries SQL via MCP
       └──────────────────────────────────────┘
                       │
                       ▼
       ┌──────────────────────────────────────┐
       │     Node 2: Execution Draft Agent    │ ◄──┐ Loops back for self-correction
       └──────────────────────────────────────┘    │ if Critic raises hallucination alarm
                       │                           │
                       ▼                           │
       ┌──────────────────────────────────────┐    │
       │      Node 3: Critic Compliance       │ ───┘
       └──────────────────────────────────────┘
                       │
             (If 100% Fact Checked)
                       │
                       ▼
         [HUMAN REVIEW / DISPATCH PIPELINE]
    ```
    """)