import streamlit as st
from background import render_background
import json

render_background()
#remove sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
[data-testid="collapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Analysis Report",layout="wide")

#button
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;500&display=swap');
div.stButton > button > div {
    background: linear-gradient(
        135deg,
        #06B6D4,
        #00FFAA
    );

    color: black;
    border: none;
    border-radius: 15px;

    padding: 12px 30px;

    font-size: 18px;
    font-weight: 600;
    font-family: 'Orbitron';

    box-shadow:
        0 0 15px rgba(37,99,235,0.5);

    transition: all 0.3s ease;
    
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 25px rgba(37,99,235,0.8);

}
div[class*="st-key-nav_"] button[type="primary"] {
    color: var(--text-primary) !important;
    background: rgba(34, 211, 238, 0.12) !important;
    border-radius: 8px !important;
    border: 1px solid #00FFAA !important;
}
</style>
""", unsafe_allow_html=True)



import os
import requests
from dotenv import load_dotenv
from prompts import website_prompt

load_dotenv()

api_key = os.getenv("api_key")

prompt = website_prompt.format(
    url=st.session_state.get("url"),
    analysis_results=st.session_state.get("analysis_results"),
    security_score=st.session_state.get("security_score"),
    privacy_score=st.session_state.get("privacy_score"),
    overall_score=st.session_state.get("overall_score")
)
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
)

response.raise_for_status()

result = response.json()

ai_text = result["choices"][0]["message"]["content"]

summary = json.loads(ai_text)

# =========================
# SHOULD I USE THIS WEBSITE?
# =========================
url = st.session_state.get("url")
st.subheader(f"🌐 Should You Use This Website- {url} ?")

recommendation = summary["usage_recommendation"]

decision = recommendation["decision"]
reason = recommendation["reason"]

if decision == "YES":
    st.success(f"🟢 YES — This website appears reasonably safe to use.")

elif decision == "MAYBE":
    st.warning(f"🟡 MAYBE — Use caution before using this website.")

else:
    st.error(f"🔴 NO — We recommend avoiding this website.")

st.write(reason)
# =========================
# OVERALL AI ASSESSMENT
# =========================

st.subheader("🛡️ CyberShield AI Assessment")

# Scores
security_score = summary["security_score"]
privacy_score = summary["privacy_score"]
overall_score = summary["overall_score"]

# Overall Score
st.metric(
    label="Overall Trust Score",
    value=f"{overall_score}/100"
)

st.progress(overall_score / 100)


# =========================
# RISK LEVEL
# =========================

risk = summary["risk_level"]

if risk == "Low":
    st.success(f"🟢 Overall Risk Level: {risk}")

elif risk == "Medium":
    st.warning(f"🟡 Overall Risk Level: {risk}")

else:
    st.error(f"🔴 Overall Risk Level: {risk}")


# =========================
# SCORE BREAKDOWN
# =========================

st.subheader("📊 Score Breakdown")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🔐 Security",
        value=f"{security_score}/100"
    )

with col2:
    st.metric(
        label="🔒 Privacy",
        value=f"{privacy_score}/100"
    )

with col3:
    st.metric(
        label="🛡️ Overall",
        value=f"{overall_score}/100"
    )


# =========================
# AI SUMMARY
# =========================

st.subheader("📋 AI Overall Summary")

st.write(summary["summary"])


# =========================
# SECURITY ASSESSMENT
# =========================

st.subheader("🔐 Security Assessment")

security_status = summary["security_status"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    if security_status["https"] == "Good":
        st.success("✓ HTTPS")
    elif security_status["https"] == "Warning":
        st.warning("⚠ HTTPS")
    else:
        st.error("✕ HTTPS")

with col2:
    if security_status["ssl_certificate"] == "Good":
        st.success("✓ SSL/TLS")
    elif security_status["ssl_certificate"] == "Warning":
        st.warning("⚠ SSL/TLS")
    else:
        st.error("✕ SSL/TLS")

with col3:
    if security_status["domain"] == "Good":
        st.success("✓ Domain")
    elif security_status["domain"] == "Warning":
        st.warning("⚠ Domain")
    else:
        st.error("✕ Domain")

with col4:
    if security_status["security_headers"] == "Good":
        st.success("✓ Security Headers")
    elif security_status["security_headers"] == "Warning":
        st.warning("⚠ Security Headers")
    else:
        st.error("✕ Security Headers")



# =========================
# PRIVACY ASSESSMENT
# =========================

st.subheader("🔒 Privacy Assessment")

privacy_status = summary["privacy_status"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    if privacy_status["cookies"] == "Good":
        st.success("✓ Cookies")
    elif privacy_status["cookies"] == "Warning":
        st.warning("⚠ Cookies")
    else:
        st.error("✕ Cookies")

with col2:
    if privacy_status["trackers"] == "Good":
        st.success("✓ Trackers")
    elif privacy_status["trackers"] == "Warning":
        st.warning("⚠ Trackers")
    else:
        st.error("✕ Trackers")

with col3:
    if privacy_status["third_party_trackers"] == "Good":
        st.success("✓ Third-Party Services")
    elif privacy_status["third_party_trackers"] == "Warning":
        st.warning("⚠ Third-Party Services")
    else:
        st.error("✕ Third-Party Services")

with col4:
    if privacy_status["data_collection"] == "Good":
        st.success("✓ Data Collection")
    elif privacy_status["data_collection"] == "Warning":
        st.warning("⚠ Data Collection")
    else:
        st.error("✕ Data Collection")


# =========================
# KEY FINDINGS
# =========================

st.subheader("⚠️ Key Findings")

for finding in summary["key_findings"]:

    title = finding["title"]
    finding_status = finding["status"]
    explanation = finding["explanation"]

    with st.expander(title):

        if finding_status == "Good":
            st.success("✓ Good")

        elif finding_status == "Warning":
            st.warning("⚠ Warning")

        else:
            st.error("✕ Risk")

        st.write(explanation)


# =========================
# RECOMMENDATIONS
# =========================

st.subheader("💡 Recommendations")

for recommendation in summary["recommendations"]:
    st.write(f"• {recommendation}")