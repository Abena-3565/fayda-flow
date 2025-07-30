import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("model/public_demand_model.pkl")

st.title("🌾 FaydaFlow - Agricultural Public Service Demand Predictor")

# Inputs
gender = st.selectbox("Gender", ["Male", "Female"])
region = st.selectbox("Region", ["Addis Ababa", "Oromia", "Amhara", "Tigray"])
zone = st.selectbox("Zone", ["Zone 1", "Zone 2", "Zone 3", "Zone 4"])
woreda = st.selectbox("Woreda", ["Woreda A", "Woreda B", "Woreda C", "Woreda D"])
occupation = st.selectbox("Occupation", ["farmer", "teacher", "trader"])
service_type = st.selectbox("Agricultural Service Type", ["fertilizer", "training", "irrigation", "crop_protection"])
week = st.slider("Week of Year", 1, 52, 27)
soil_quality = st.slider("Soil Quality Score", 1, 5)
rainfall = st.slider("Rainfall (mm)", 0, 100, 60)
crop_price = st.slider("Crop Price Index", 80, 150, 100)
drought_risk = st.slider("Drought Risk Index", 1, 5, 2)

# Convert to DataFrame
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

# Fill missing columns with 0
model_features = model.feature_names_in_
row = pd.DataFrame([{col: input_dict.get(col, 0) for col in model_features}])

if st.button("Predict Demand"):
    prediction = model.predict(row)[0]
    st.success(f"📈 Predicted Public Service Demand: {int(prediction)}")
