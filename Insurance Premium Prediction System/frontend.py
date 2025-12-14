import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Category Prediction")
st.markdown("Enter your details below")

# Input Fields
age = st.number_input("Age", min_value=1, max_value=75, value=30)
weight = st.number_input("Weight (Kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.8, value=1.70)
income_lpa = st.number_input("Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=["yes", "no"])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox("Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

if st.button("Predict Premium Category"):
    user_input = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=user_input, timeout=10)
        result = response.json()

        if response.status_code == 200 and "response" in result:
            prediction = result["response"]
            st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
            st.write("Confidence:", prediction["confidence"])
            st.write("Class Probabilities:")
            st.json(prediction["class_probabilities"])

        
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exception.ConnectionError:
        st.error("Could not connect to the FastAPI Server. Make sure it's running.")