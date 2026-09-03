import streamlit as st
from background import render_background

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

.stButton > button {
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
    text-align: center;
            
    box-shadow:
        0 0 15px rgba(37,99,235,0.5);

    transition: all 0.3s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 25px rgba(37,99,235,0.8);

}

</style>
""", unsafe_allow_html=True)

import os
import requests
from dotenv import load_dotenv
from prompts import android_prompt
import json
load_dotenv()

api_key = os.getenv("api_key")

prompt = android_prompt.format(
    app_name=st.session_state["app_name"],
    analysis_results=st.session_state["analysis_results"],
    security_score=st.session_state["security_score"],
    privacy_score=st.session_state["privacy_score"],
    overall_score=st.session_state["overall_score"]
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
# IPHONE APP OVERALL ASSESSMENT
# =========================

st.subheader("🛡️ CyberShield AI Assessment")

# Scores
security_score = summary.get("security_score", 0)
privacy_score = summary.get("privacy_score", 0)
overall_score = summary.get("overall_score", 0)


# =========================
# OVERALL SCORE
# =========================

st.metric(
    label="Overall Trust Score",
    value=f"{overall_score}/100"
)

st.progress(overall_score / 100)


# =========================
# RISK LEVEL
# =========================

risk = summary.get("risk_level", "Medium")

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
# AI OVERALL SUMMARY
# =========================

st.subheader("📋 AI Overall Summary")

st.write(
    summary.get(
        "summary",
        "No overall summary was generated."
    )
)


# =========================
# SECURITY ASSESSMENT
# =========================

st.subheader("🔐 Security Assessment")

security_status = summary.get("security_status", {})

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    status = security_status.get("permissions", "Warning")

    if status == "Good":
        st.success("✓ Permissions")
    elif status == "Warning":
        st.warning("⚠ Permissions")
    else:
        st.error("✕ Permissions")


with col2:
    status = security_status.get("app_signature", "Warning")

    if status == "Good":
        st.success("✓ Signature")
    elif status == "Warning":
        st.warning("⚠ Signature")
    else:
        st.error("✕ Signature")


with col3:
    status = security_status.get("network_security", "Warning")

    if status == "Good":
        st.success("✓ Network")
    elif status == "Warning":
        st.warning("⚠ Network")
    else:
        st.error("✕ Network")


with col4:
    status = security_status.get("suspicious_behavior", "Warning")

    if status == "Good":
        st.success("✓ Behavior")
    elif status == "Warning":
        st.warning("⚠ Behavior")
    else:
        st.error("✕ Behavior")


with col5:
    status = security_status.get("integrity", "Warning")

    if status == "Good":
        st.success("✓ Integrity")
    elif status == "Warning":
        st.warning("⚠ Integrity")
    else:
        st.error("✕ Integrity")


# =========================
# PRIVACY ASSESSMENT
# =========================

st.subheader("🔒 Privacy Assessment")

privacy_status = summary.get("privacy_status", {})

col1, col2, col3, col4 = st.columns(4)

with col1:
    status = privacy_status.get("data_collection", "Warning")

    if status == "Good":
        st.success("✓ Data Collection")
    elif status == "Warning":
        st.warning("⚠ Data Collection")
    else:
        st.error("✕ Data Collection")


with col2:
    status = privacy_status.get("trackers", "Warning")

    if status == "Good":
        st.success("✓ Trackers")
    elif status == "Warning":
        st.warning("⚠ Trackers")
    else:
        st.error("✕ Trackers")


with col3:
    status = privacy_status.get("third_party_services", "Warning")

    if status == "Good":
        st.success("✓ Third-Party Services")
    elif status == "Warning":
        st.warning("⚠ Third-Party Services")
    else:
        st.error("✕ Third-Party Services")


with col4:
    status = privacy_status.get("sensitive_permissions", "Warning")

    if status == "Good":
        st.success("✓ Sensitive Permissions")
    elif status == "Warning":
        st.warning("⚠ Sensitive Permissions")
    else:
        st.error("✕ Sensitive Permissions")


# =========================
# KEY FINDINGS
# =========================

st.subheader("⚠️ Key Findings")

for finding in summary.get("key_findings", []):

    title = finding.get("title", "Finding")
    finding_status = finding.get("status", "Warning")
    explanation = finding.get(
        "explanation",
        "No explanation available."
    )

    category = finding.get("category", "Overall")

    with st.expander(f"{title} — {category}"):

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

for recommendation in summary.get("recommendations", []):

    st.write(f"• {recommendation}")