import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# --- App Configuration ---
st.set_page_config(
    page_title="FaydaFlow | Agricultural Demand Predictor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"  # Control sidebar initial state
)

# --- Custom CSS ---
st.markdown("""
<style>
    .css-18e3th9 {padding: 2rem 5rem;}
    .stSelectbox, .stSlider {margin-bottom: 1.5rem;}
    .stButton>button {background-color: #2e86c1; color: white; border-radius: 8px; padding: 0.5rem 1rem;}
    .stSuccess {background-color: #d5f5e3; border-left: 5px solid #28b463; padding: 1rem;}
    .metric-card {padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    [data-testid="stSidebar"] {transition: all 0.3s ease;}
    .sidebar-collapsed {transform: translateX(-100%); width: 0 !important;}
</style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'sidebar_collapsed' not in st.session_state:
    st.session_state.sidebar_collapsed = False

# --- Sidebar with Authentication ---
def show_sidebar():
    with st.sidebar:
        st.image("assets/nid-logo.png", width=150)
        st.title("Fayda ID Login")
        fayda_id = st.text_input("Enter Fayda ID")
        if st.button("Login", type="primary"):
            if fayda_id:  # Simple validation - replace with actual auth
                st.session_state.authenticated = True
                st.session_state.sidebar_collapsed = True
                st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.info("This tool predicts demand for agricultural services using Ethiopia's Fayda ID system.")

# Show sidebar only if not authenticated or not collapsed
if not st.session_state.authenticated or not st.session_state.sidebar_collapsed:
    show_sidebar()

# Apply sidebar collapse style
if st.session_state.sidebar_collapsed:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            .main .block-container {
                padding-left: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Main App ---
if st.session_state.authenticated:
    st.title("🌾 FaydaFlow Agricultural Service Demand Predictor")
    st.caption("Optimizing public service delivery through AI and national ID integration")

    # --- Input Section ---
    col1, col2 = st.columns(2)

    with col1:
        st.header("Farmer Details")
        gender = st.selectbox("Gender", ["Male", "Female"])
        region = st.selectbox("Region", ["Addis Ababa", "Oromia", "Amhara", "Tigray"])
        zone = st.selectbox("Zone", ["Zone 1", "Zone 2", "Zone 3", "Zone 4"])
        woreda = st.selectbox("Woreda", ["Woreda A", "Woreda B", "Woreda C", "Woreda D"])
        occupation = st.selectbox("Occupation", ["farmer", "teacher", "trader"])

    with col2:
        st.header("Agricultural Conditions")
        service_type = st.selectbox("Service Type", ["fertilizer", "training", "irrigation", "crop_protection"])
        week = st.slider("Week of Year", 1, 52, 27, help="Current week in the agricultural cycle")
        soil_quality = st.slider("Soil Quality (1-5)", 1, 5, 3, 
                                help="1 = Poor, 5 = Excellent")
        rainfall = st.slider("Rainfall (mm)", 0, 100, 60)
        crop_price = st.slider("Crop Price Index", 80, 150, 100)
        drought_risk = st.slider("Drought Risk (1-5)", 1, 5, 2)

    # --- Load Model ---
    @st.cache_resource
    def load_model():
        try:
            return joblib.load("model/public_demand_model.pkl")
        except Exception as e:
            st.error(f"Failed to load model: {str(e)}")
            return None

    model = load_model()

    # --- Prediction Logic ---
    if st.button("📊 Predict Service Demand", type="primary") and model is not None:
        with st.spinner("Analyzing agricultural patterns..."):
            try:
                # Prepare input data
                input_dict = {
                    "week_of_year": week,
                    "soil_quality_score": soil_quality,
                    "rainfall_mm": rainfall,
                    "crop_price_index": crop_price,
                    "drought_risk_index": drought_risk,
                    f"gender_{gender}": 1,
                    f"region_{region}": 1,
                    f"zone_{zone}": 1,
                    f"woreda_{woreda}": 1,
                    f"occupation_{occupation}": 1,
                    f"service_type_{service_type}": 1
                }
                
                model_features = model.feature_names_in_
                row = pd.DataFrame([{col: input_dict.get(col, 0) for col in model_features}])
                
                # Make prediction
                prediction = model.predict(row)[0]
                
                # Display results
                st.success(f"Predicted Demand: **{int(prediction)} service units** needed in {woreda}")
                
                # --- Visualization ---
                st.markdown("---")
                st.header("Regional Demand Insights")
                
                # Mock historical data (replace with your actual data)
                historical_data = pd.DataFrame({
                    "Week": range(1, 53),
                    "Demand": [max(0, prediction * 0.7 + i * 2) for i in range(52)]
                })
                
                fig = px.line(historical_data, x="Week", y="Demand", 
                             title=f"Seasonal Demand Pattern for {service_type}",
                             labels={"Demand": "Service Units Needed"})
                st.plotly_chart(fig, use_container_width=True)
                
                # --- Recommendation Engine ---
                st.markdown("---")
                st.header("Recommended Actions")
                
                if drought_risk >= 4:
                    st.warning("🚨 High drought risk detected!")
                    st.markdown("""
                    - Prioritize irrigation support
                    - Distribute drought-resistant seeds
                    - Activate emergency water supply
                    """)
                
                if soil_quality <= 2:
                    st.warning("⚠️ Poor soil quality detected")
                    st.markdown("""
                    - Recommend soil testing
                    - Schedule fertilizer distribution
                    - Provide composting training
                    """)
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")

    # --- Footer ---
    st.markdown("---")
    st.caption("© 2025 FaydaFlow | Developed by Abenezer Alemayehu for Fayda Hackathon")

    # Add logout button at bottom
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.sidebar_collapsed = False
        st.rerun()