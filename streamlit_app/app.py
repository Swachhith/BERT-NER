import streamlit as st
import requests
from requests.auth import HTTPBasicAuth  # For Basic Authentication

# Streamlit UI Setup
st.title("🧠 Named Entity Recognition (NER) Tool")
st.markdown("Enter text below to extract named entities:")

# Text Input
user_input = st.text_area("Enter your text here:", height=150)

# Authentication Inputs
st.sidebar.title("🔐 Authentication")
username = st.sidebar.text_input("Username", value="", type="default")
password = st.sidebar.text_input("Password", value="", type="password")

# Prediction Button
if st.button("Predict Entities"):
    if user_input.strip():
        if not username or not password:
            st.warning("Please provide authentication details in the sidebar.")
        else:
            try:
                # Send data to FastAPI endpoint with authentication
                response = requests.post(
                    "http://flask_api:8000/predict",  # Use the service name from docker-compose.yml
                    json={"text": user_input},
                    auth=HTTPBasicAuth(username, password)
                )


                if response.status_code == 200:
                    entities = response.json().get("entities", [])
                    if entities:
                        st.success("Entities Found:")
                        for entity in entities:
                            st.markdown(f"- **{entity['text']}** → {entity['label']}")
                    else:
                        st.warning("No entities found.")
                elif response.status_code == 401:
                    st.error("🚫 Unauthorized: Please check your username and password.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Error connecting to the API: {e}")
    else:
        st.warning("Please enter some text before predicting.")
