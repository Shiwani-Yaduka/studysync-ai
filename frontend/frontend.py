import streamlit as st
import requests
from datetime import datetime

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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main {
    background-color: #07090f;
    color: #e2e8f0;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ── Hero ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.2rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 60%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.hero-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 300;
    margin-bottom: 0;
    line-height: 1.7;
}

/* ── Metric Cards ── */
.metric-card {
    position: relative;
    overflow: hidden;
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 24px 20px 20px;
    text-align: center;
    color: white;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: #3b82f6;
}

.metric-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top left, rgba(96,165,250,0.08), transparent 70%);
    pointer-events: none;
}

.metric-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}

.metric-label {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #e2e8f0;
    margin-bottom: 4px;
}

.metric-status {
    display: inline-block;
    background: rgba(34,197,94,0.12);
    color: #4ade80;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 2px 10px;
    border-radius: 99px;
    border: 1px solid rgba(74,222,128,0.25);
    letter-spacing: 0.5px;
}

/* ── Event Cards ── */
.card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-left: 3px solid #3b82f6;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.card:hover {
    background: #131f35;
    border-left-color: #60a5fa;
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #f1f5f9;
    margin: 0 0 10px;
}

.card-meta {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}

.card-meta span {
    color: #94a3b8;
    font-size: 0.83rem;
}

.badge {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 3px 12px;
    border-radius: 99px;
}

.badge-green {
    background: rgba(34,197,94,0.1);
    color: #4ade80;
    border: 1px solid rgba(74,222,128,0.2);
}

.badge-yellow {
    background: rgba(234,179,8,0.1);
    color: #facc15;
    border: 1px solid rgba(250,204,21,0.2);
}

/* ── Section Headings ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.3rem;
    color: #e2e8f0;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Divider ── */
hr {
    border-color: #1e293b !important;
    margin: 2rem 0 !important;
}

/* ── Health Grid ── */
.health-item {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    font-size: 0.9rem;
    color: #cbd5e1;
}

.health-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 6px #4ade80;
    flex-shrink: 0;
}

/* ── Streamlit overrides ── */
.stTextInput > div > div > input {
    background-color: #111827 !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    padding: 12px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    padding: 12px 24px !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

.stAlert {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown('<div class="hero-title">📚 StudySync AI</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">'
    'Your intelligent AI-powered study assistant — automatically tracks exams, '
    'generates study guides, and emails them before your deadlines.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()

# ---------------------------------------------------
# TOP METRICS
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-label">AI Automation</div>
        <span class="metric-status">Active</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">☸</div>
        <div class="metric-label">Kubernetes</div>
        <span class="metric-status">Running</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">🚀</div>
        <div class="metric-label">CI/CD Pipeline</div>
        <span class="metric-status">Connected</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# EVENTS SECTION
# ---------------------------------------------------

st.markdown('<div class="section-heading">📅 Upcoming Study Events</div>', unsafe_allow_html=True)

try:
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
                except Exception:
                    days_left = "?"

                if isinstance(days_left, int) and days_left >= 7:
                    badge = '<span class="badge badge-green">🟢 Guide Scheduled</span>'
                else:
                    badge = '<span class="badge badge-yellow">🟡 Processing Soon</span>'

                st.markdown(f"""
                <div class="card">
                    <p class="card-title">{title}</p>
                    <div class="card-meta">
                        <span>📅 {event_date}</span>
                        <span>⏳ {days_left} days remaining</span>
                    </div>
                    {badge}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No upcoming study events found.")
    else:
        st.error("Failed to fetch events from backend.")

except Exception as e:
    st.error(f"Backend connection failed: {e}")

st.divider()

# ---------------------------------------------------
# GUIDE GENERATION
# ---------------------------------------------------

st.markdown('<div class="section-heading">🧠 Generate Instant Study Guide</div>', unsafe_allow_html=True)

topic = st.text_input(
    "Topic",
    placeholder="e.g. Operating Systems Unit 5",
    label_visibility="collapsed"
)

if st.button("✨ Generate AI Study Guide", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic before generating.")
    else:
        with st.spinner("Generating your AI-powered study guide…"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={"topic": topic}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success("Study guide generated successfully!")
                    st.markdown("### 📖 Generated Guide")
                    st.markdown(data["guide"])
                else:
                    st.error(response.text)

            except Exception as e:
                st.error(f"Generation failed: {e}")

st.divider()

# ---------------------------------------------------
# SYSTEM HEALTH
# ---------------------------------------------------

st.markdown('<div class="section-heading">🛠 System Health</div>', unsafe_allow_html=True)

health_col1, health_col2 = st.columns(2)

with health_col1:
    st.markdown('<div class="health-item"><div class="health-dot"></div> Backend Connected</div>', unsafe_allow_html=True)
    st.markdown('<div class="health-item"><div class="health-dot"></div> Scheduler Running</div>', unsafe_allow_html=True)

with health_col2:
    st.markdown('<div class="health-item"><div class="health-dot"></div> Email Service Active</div>', unsafe_allow_html=True)
    st.markdown('<div class="health-item"><div class="health-dot"></div> Kubernetes Healthy</div>', unsafe_allow_html=True)