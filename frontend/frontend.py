import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://backend-service:5000"

st.set_page_config(
    page_title="StudySync  AI",
    layout="wide"
)

st.title("📚 StudySync AI Dashboard")

# -------------------------------
# Upcoming Events
# -------------------------------

st.header("📅 Upcoming Events")

try:
    response = requests.get(f"{BACKEND_URL}/events")

    if response.status_code == 200:
        events = response.json()

        if events:
            df = pd.DataFrame(events)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No upcoming events found")

    else:
        st.error("Failed to fetch events")

except Exception as e:
    st.error(str(e))

# -------------------------------
# Manual Guide Generation
# -------------------------------

st.header("🧠 Generate Study Guide")

topic = st.text_input("Enter topic")

if st.button("Generate Guide"):

    with st.spinner("Generating AI study guide..."):

        response = requests.post(
            f"{BACKEND_URL}/generate",
            json={"topic": topic}
        )

        if response.status_code == 200:

            data = response.json()

            st.success("Guide Generated")

            st.markdown(data["guide"])

        else:
            st.error(response.json())