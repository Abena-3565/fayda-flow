# **FaydaFlow: ML-Driven Public Resource Allocation for Smart Governance**

A machine learning platform designed to support smarter, more equitable public service delivery in Ethiopia.

---

## Contributor:
- Abenezer Alemayeh

### **Project Synopsis**  

### Problem Statement:
Government agencies struggle to deploy public services like agriculture, healthcare, education, and food aid resources efficiently due to:
- Manual workflows prone to bias or delays
- Inadequate forecasting (reaction > prediction)
- Lack of real-time, identity-linked data

### Planned Solution:
An ML system that **predicts demand for public services** using:  
1. **Fayda ID-linked data** (demographics, location, historical service usage).  
2. **External datasets** (e.g., weather, disease outbreaks, economic indicators).  
3. **Models:**  
   - **Time-series forecasting** (ARIMA, Prophet) for healthcare/subsidy demand.  
   - **Clustering (k-means)** to identify high-need regions.  

### Expected Outcome:
- A working ML model to forecast regional service demand
- A dashboard showing predicted "hotspots" for resource allocation
- Faster response to emergent needs

---

### Fayda's Role:
- **Anchor data:** Use anonymized Fayda ID attributes (age, location, occupation) to personalize predictions.  
- **Verification:** Integrate **VeriFayda OIDC** to demo secure access for government workers.
- Helps filter duplicate/fake service requests

## Tech Stack:
- Python
- Scikit-learn / XGBoost
- Pandas / NumPy
- Streamlit (for dashboard)
- SQLite or CSVs (mock database)
- VeriFayda OIDC API (identity integration)
- GitHub Actions (optional CI/CD)

## How to Run:
# Clone repo
git clone https://github.com/Abena-3565/fayda-flow.git

cd fayda-flow

# Install dependencies
pip install -r requirements.txt

# Train ML model
python model/train.py

# Launch dashboard
streamlit run app.py
