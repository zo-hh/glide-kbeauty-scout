import streamlit as st
import pandas as pd
import json
import os
import time
import subprocess
import sys
import streamlit as st

# Inject Streamlit secrets into environment variables for subprocess compatibility in the cloud
try:
    for k, v in st.secrets.items():
        if isinstance(v, str):
            os.environ[k] = v
except Exception:
    pass

# Import the core logic from existing scripts
import export

# Pre-populated list of ~90 prominent K-Beauty brands
BRANDS_LIST = sorted([
    "COSRX", "AMUSE", "CENTELLIAN24", "AHC", "CELL FUSION C", "LANEIGE", "MAMONDE", "SOME BY MI", "ANUA", "HANYUL", 
    "TONYMOLY", "MEDICUBE", "SULWHASOO", "ABIB", "IOPE", "SKINFOOD", "AXIS-Y", "APIEU", "BEAUTY OF JOSEON", "DR.JART+", 
    "ISNTREE", "PURITO", "SKIN1004", "MIXSOON", "TORRIDEN", "ROUND LAB", "ILLIYOON", "NUMBUZIN", "I'M FROM", "KLAIRS", 
    "BY WISHTREND", "ROVECTIN", "TIRTIR", "ROM&ND", "PERIPERA", "CLIO", "3CE", "ETUDE HOUSE", "NATURE REPUBLIC", 
    "THE FACE SHOP", "MISSHA", "BANILA CO", "HEIMISH", "GOODAL", "MA:NYO", "NEOGEN", "BENTON", "PYUNKANG YUL", 
    "HADA LABO", "MARY&MAY", "JUMISO", "CELIMAX", "NACIFIC", "TIA'M", "SIORIS", "HUXLEY", "KEEP COOL", "MAKER", 
    "WAKEMAKE", "HOLIKA HOLIKA", "TOO COOL FOR SCHOOL", "VT COSMETICS", "D'ALBA", "HARUHARU WONDER", "DEAR, KLAIRS", 
    "CORSX", "PEACH SLICES", "PEACH & LILY", "GLOW RECIPE", "SATURDAY SKIN", "THEN I MET YOU", "SOKO GLAM", "BEAUTY PIE", 
    "BLIND", "BOUQUET GARNI", "CATCHING", "DERMATORY", "EQUILIBRIUM", "FLASKIN", "HERA", "JUNG SAEM MOOL", "LAKA", 
    "MERZY", "NONFICTION", "O HUI", "PONY EFFECT", "REJURAN", "SUM37", "TAMBURINS", "VDL", "TOCOBO"
])

# Set Streamlit page config
st.set_page_config(
    page_title="Glide K-Beauty Scout",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom premium CSS
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    h1 {
        color: #2563eb;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        border-color: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37,99,235,0.4);
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Glide K-Beauty Brand Scout")
st.markdown("<h3 style='color: #10b981; font-style: italic; margin-top: -15px; margin-bottom: 20px;'>by Zuhrat Ul Wardh</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: #e2e8f0; font-size: 1.1rem;'>Select up to <b style='color: #f59e0b;'>5 brands</b> from the curated list below. The <span style='color: #8b5cf6; font-weight: bold;'>AI pipeline</span> will fetch live web data, evaluate their market fit for India, and display the results!</p>", unsafe_allow_html=True)

st.sidebar.header("Brand Selection")
selected_brands = st.sidebar.multiselect(
    "Choose Brands to Evaluate:",
    options=BRANDS_LIST,
    max_selections=5,
    help="You can select up to 5 brands at a time to stay within API limits."
)

if "evaluation_completed" not in st.session_state:
    st.session_state.evaluation_completed = False

if st.sidebar.button("Run Evaluation"):
    if not selected_brands:
        st.error("Please select at least one brand from the dropdown.")
    else:
        with st.spinner("Pipeline running... Fetching web data and calling Groq LLM!"):
            with open("brands_list.json", "w", encoding="utf-8") as f:
                json.dump(selected_brands, f)
            
            try:
                subprocess.run([sys.executable, "evaluation.py"], check=True)
                st.session_state.evaluation_completed = True
            except Exception as e:
                st.error(f"Pipeline execution failed: {str(e)}")

# Display results outside the button block so they persist!
if st.session_state.evaluation_completed:
    if os.path.exists("evaluated_brands.json"):
        with open("evaluated_brands.json", "r", encoding="utf-8") as f:
            results = json.load(f)
        
        df = pd.DataFrame(results)
        st.success("✅ Evaluation complete!")
        
        st.subheader("Market Evaluation Results")
        # Clean the table for display
        df_display = df.drop(columns=["Justification", "Key_Ingredients", "Total_Glide_Fit_Score_40"])
        
        st.dataframe(
            df_display.style.format({'Glide_Fit_Score_10': "{:.1f}"}).background_gradient(cmap='RdYlGn', subset=['Glide_Fit_Score_10']),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        st.subheader("📊 Deep Dive Reports")
        st.markdown("Select a brand from the table above to view its detailed analytical justification and ingredient risk profile.")
        
        selected_report = st.selectbox("Select Brand:", df["Brand"].tolist())
        
        if selected_report:
            brand_data = df[df["Brand"] == selected_report].iloc[0]
            st.info(f"### {brand_data['Brand']}")
            
            col1, col2 = st.columns(2)
            col1.metric("Glide Fit (/10)", f"{brand_data['Glide_Fit_Score_10']:.1f}")
            col2.metric("Risk Level", brand_data['Risk_Level'])
            
            st.markdown(f"**📝 Analyst Justification:**\n> *{brand_data['Justification']}*")
            
            price_safe = str(brand_data['Est_Price']).replace('$', r'\$')
            st.markdown(f"**🌟 Hero Product:** {brand_data['Hero_Product']}  |  **💰 Price:** {price_safe}")
            st.markdown(f"**🧪 Key Ingredients:** {brand_data['Key_Ingredients']}")
        
        st.markdown("---")
        st.markdown("### 📥 Export Data")
        
        # Convert df to CSV for download
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name='glide_kbeauty_shortlist.csv',
            mime='text/csv',
        )

st.markdown("---")
st.caption("Powered by Apify, Groq Llama-3.3, and Streamlit.")
