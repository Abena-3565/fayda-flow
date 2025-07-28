import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("model/public_demand_model.pkl")

st.title("📊 FaydaFlow - Predict Public Service Demand")
st.markdown("Use Fayda ID-linked inputs to forecast public service needs.")

# Input form
region_code = st.selectbox("Region Code", [101, 102, 103, 104])
week_of_year = st.slider("Week of the Year", 1, 52, 27)
age_group = st.selectbox("Age Group", ["18-25", "26-35", "36-50"])
occupation = st.selectbox("Occupation", ["farmer", "teacher", "trader"])
service_type = st.selectbox("Service Type", ["healthcare", "education", "food_aid", "ID_service"])

if st.button("Predict Demand"):
    # Create input DataFrame
    input_data = pd.DataFrame({
        "region_code": [region_code],
        "week_of_year": [week_of_year],
        "age_group_26-35": [1 if age_group == "26-35" else 0],
        "age_group_36-50": [1 if age_group == "36-50" else 0],
        "occupation_teacher": [1 if occupation == "teacher" else 0],
        "occupation_trader": [1 if occupation == "trader" else 0],
        "service_type_food_aid": [1 if service_type == "food_aid" else 0],
        "service_type_healthcare": [1 if service_type == "healthcare" else 0],
        "service_type_ID_service": [1 if service_type == "ID_service" else 0]
    })

    # Predict
    prediction = model.predict(input_data)[0]
    st.success(f"🔮 Predicted Service Demand: **{int(prediction)}** people")
