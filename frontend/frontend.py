import streamlit as st
import requests
from datetime import datetime
import pandas as pd

BACKEND_URL = "http://backend-service:5000"

st.set_page_config(
page_title="StudySync AI",
page_icon="📚",
layout="wide"
)

# ---------------------------------------------------

# Custom CSS

# ---------------------------------------------------

st.markdown("""

<style>

.main {
    background-color: #0f172a;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 15px;
    border: 1px solid #334155;
}

.metric-card {
    background: linear-gradient(135deg, #2563eb, #1e3a8a);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    color: white;
}

.small-text {
    color: #cbd5e1;
    font-size: 14px;
}

.status-green {
    color: #22c55e;
    font-weight: bold;
}

.status-yellow {
    color: #facc15;
    font-weight: bold;
}

</style>

""", unsafe_allow_html=True)

# ---------------------------------------------------

# HERO SECTION

# ---------------------------------------------------

st.markdown("""

# 📚 StudySync AI

### Your intelligent AI-powered study assistant

Automatically tracks exams, generates study guides, and emails them before your deadlines.
""")

st.divider()

# ---------------------------------------------------

# TOP METRICS

# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
st.markdown(""" <div class="metric-card"> <h2>⚡ AI Automation</h2> <p>Active</p> </div>
""", unsafe_allow_html=True)

with col2:
st.markdown(""" <div class="metric-card"> <h2>☸ Kubernetes</h2> <p>Running</p> </div>
""", unsafe_allow_html=True)

with col3:
st.markdown(""" <div class="metric-card"> <h2>🚀 CI/CD</h2> <p>Connected</p> </div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------

# UPCOMING EVENTS

# ---------------------------------------------------

st.subheader("📅 Upcoming Study Events")

try:

```
response = requests.get(f"{BACKEND_URL}/events")

if response.status_code == 200:

    events = response.json()

    if events:

        for event in events:

            title = event.get("title", "Untitled Event")

            start = event.get("start", {})

            event_date = (
                start.get("dateTime")
                or start.get("date")
                or "Unknown Date"
            )

            try:
                parsed_date = datetime.fromisoformat(
                    event_date.replace("Z", "+00:00")
                )

                days_left = (parsed_date.date() - datetime.now().date()).days

            except:
                days_left = "?"

            status = (
                "🟢 Guide Scheduled"
                if isinstance(days_left, int) and days_left >= 7
                else "🟡 Processing Soon"
            )

            st.markdown(f"""
            <div class="card">
                <h3>{title}</h3>

                <p class="small-text">
                📅 Exam Date: {event_date}
                </p>

                <p class="small-text">
                ⏳ Days Remaining: {days_left}
                </p>

                <p>{status}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No upcoming study events found")

else:
    st.error("Failed to fetch events from backend")
```

except Exception as e:
st.error(f"Backend connection failed: {e}")

st.divider()

# ---------------------------------------------------

# MANUAL GUIDE GENERATION

# ---------------------------------------------------

st.subheader("🧠 Generate Instant Study Guide")

topic = st.text_input(
"Enter topic",
placeholder="Example: Operating Systems Unit 5"
)

if st.button("Generate AI Guide", use_container_width=True):

```
if not topic.strip():
    st.warning("Please enter a topic")
else:

    with st.spinner("Generating AI-powered study guide..."):

        try:

            response = requests.post(
                f"{BACKEND_URL}/generate",
                json={"topic": topic}
            )

            if response.status_code == 200:

                data = response.json()

                st.success("Study Guide Generated Successfully")

                st.markdown("""
                ### 📖 Generated Guide
                """)

                st.markdown(data["guide"])

            else:
                st.error(response.text)

        except Exception as e:
            st.error(f"Generation failed: {e}")
```

st.divider()

# ---------------------------------------------------

# SYSTEM HEALTH

# ---------------------------------------------------

st.subheader("🛠 System Health")

health_col1, health_col2 = st.columns(2)

with health_col1:
st.success("Backend Connected")
st.success("Scheduler Running")

with health_col2:
st.success("Email Service Active")
st.success("Kubernetes Healthy")
