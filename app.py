import streamlit as st
import pandas as pd
import numpy as np
import os
from model import train_model, predict
from fairness import calculate_fairness
from interceptor import intercept_decision
from database import init_db, log_decision
from simulation import simulate_change
from report import generate_report

# Setup
init_db()
st.set_page_config(page_title="FairAI LiveGuard PRO", layout="wide", page_icon="🛡️")

# PREMIUM CYBER-GLOW STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2c, #0e1117);
    }
    
    .main-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: -webkit-linear-gradient(#00ffcc, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ffcc;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0099ff);
        color: #0e1117 !important;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        height: 3.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🛡️ FairAI LiveGuard</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #888; font-size: 1.2rem; margin-bottom: 2rem;">Enterprise AI Governance & Ethics Firewall</p>', unsafe_allow_html=True)

st.sidebar.title("🛰️ CONTROL CENTER")
page = st.sidebar.radio("Navigation", ["Overview & Upload", "AI Fairness Lab", "Governance & Audit"])

if page == "Overview & Upload":
    st.subheader("📂 Data Ingestion Portal")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload CSV Training Data", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.session_state['df'] = df
            st.success("✅ Dataset Ingested Successfully")
            st.dataframe(df.head(10), use_container_width=True)
        else:
            st.info("👋 Welcome! Start by uploading your dataset or use a demo below.")
            
    with col2:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.write("### 🚀 Quick Load")
        if st.button("Load Hiring Demo"):
            st.session_state['df'] = pd.read_csv("data/hiring_sample.csv")
            st.rerun()
        if st.button("Load Loan Demo"):
            st.session_state['df'] = pd.read_csv("data/loan_sample.csv")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "AI Fairness Lab":
    if 'df' not in st.session_state:
        st.error("Please upload data in the 'Overview' tab first.")
    else:
        df = st.session_state['df']
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.header("⚙️ Config")
            target = st.selectbox("Target Label", df.columns, index=len(df.columns)-1)
            sensitive = st.selectbox("Sensitive Feature", df.columns, index=1)
            threshold = st.slider("Bias Tolerance", 0.0, 0.5, 0.15)
            
            if st.button("⚡ ANALYZE SYSTEM"):
                with st.spinner("Calculating Metrics..."):
                    model, X, y = train_model(df, target)
                    st.session_state['model'] = model
                    st.session_state['sensitive'] = sensitive
                    st.session_state['threshold'] = threshold
                    
                    preds = model.predict(X)
                    score = calculate_fairness(y, preds, X[sensitive])
                    st.session_state['fairness_score'] = score
                    
                    # Group-wise data for chart
                    dist = pd.DataFrame({'Group': X[sensitive], 'Outcome': preds})
                    st.session_state['dist_data'] = dist.groupby('Group')['Outcome'].mean()
                    st.success("Analysis Complete!")

        with col2:
            st.header("⚖️ Fairness Dashboard")
            if 'fairness_score' in st.session_state:
                m1, m2 = st.columns(2)
                with m1:
                    score = st.session_state['fairness_score']
                    color = "#ff4b4b" if score > threshold else "#00ffcc"
                    st.markdown('<div class="status-card">', unsafe_allow_html=True)
                    st.write("Bias Score")
                    st.markdown(f'<p class="metric-value" style="color: {color}">{score:.4f}</p>', unsafe_allow_html=True)
                    st.write("Status: " + ("🚨 CRITICAL" if score > threshold else "✅ SAFE"))
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with m2:
                    st.write("Outcome Distribution")
                    st.bar_chart(st.session_state['dist_data'])

        if 'model' in st.session_state:
            st.divider()
            st.subheader("🛡️ Real-Time Prediction Interceptor")
            input_cols = [c for c in df.columns if c != target]
            user_input = {}
            ui_cols = st.columns(len(input_cols))
            for i, col in enumerate(input_cols):
                user_input[col] = ui_cols[i].number_input(f"{col}", value=float(df[col].mean()))
            
            if st.button("Check Decision"):
                result = predict(st.session_state['model'], user_input)
                status = intercept_decision(result, st.session_state['fairness_score'], st.session_state['threshold'])
                
                log_decision(user_input, result, status)
                
                if status == "BLOCKED":
                    st.error(f"🛑 BIAS FIREWALL: Decision Blocked. The prediction ({result}) is likely influenced by sensitive attributes.")
                    if st.checkbox("Admin Override"):
                        st.success(f"🔓 Human Approved: {result}")
                else:
                    st.success(f"✅ APPROVED: Decision is safe to proceed. Prediction: {result}")

            st.divider()
            st.subheader("🔁 Scenario Simulator ('What-If')")
            if st.button("Simulate Alternative Group Outcome"):
                s_feat = st.session_state['sensitive']
                orig_val = user_input[s_feat]
                new_val = 1 - orig_val if orig_val in [0, 1] else orig_val + 1
                
                sim_input = simulate_change(user_input, s_feat, new_val)
                sim_res = predict(st.session_state['model'], sim_input)
                
                st.info(f"Original Group ({s_feat}={orig_val}) Result: **{predict(st.session_state['model'], user_input)}**")
                st.info(f"Counterfactual Group ({s_feat}={new_val}) Result: **{sim_res}**")
                if sim_res != predict(st.session_state['model'], user_input):
                    st.error("⚠️ BIAS CONFIRMED: Changing the sensitive feature changes the outcome!")

elif page == "Governance & Audit":
    st.header("🧾 Compliance & Governance Logs")
    if os.path.exists("logs.db"):
        import sqlite3
        conn = sqlite3.connect("logs.db")
        logs_df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
        conn.close()
        
        if not logs_df.empty:
            st.dataframe(logs_df, use_container_width=True)
            
            st.subheader("📈 Decision Trends")
            st.bar_chart(logs_df['status'].value_counts())
            
            if st.button("📄 Generate PDF Audit Report"):
                audit_summary = f"""
                Compliance Report Summary
                -------------------------
                Total Decisions Analyzed: {len(logs_df)}
                Decisions Approved: {len(logs_df[logs_df['status'] == 'APPROVED'])}
                Decisions Blocked (Bias): {len(logs_df[logs_df['status'] == 'BLOCKED'])}
                
                Summary: This system is operating under real-time fairness monitoring.
                All blocked decisions were flagged by the Interceptor Layer using Demographic Parity metrics.
                """
                filename = generate_report(audit_summary)
                with open(filename, "rb") as f:
                    st.download_button("Download Audit PDF", f, file_name="LiveGuard_Audit.pdf")
        else:
            st.info("No logs yet. Run some predictions in the Lab!")
    else:
        st.info("Governance database not yet initialized.")
