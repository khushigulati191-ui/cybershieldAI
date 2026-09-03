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


import os
import requests
from dotenv import load_dotenv
from prompts import website_comparison_prompt

load_dotenv()

api_key = os.getenv("api_key")

prompt = website_comparison_prompt.format(
    website1_data=st.session_state["website1_data"],
    website2_data=st.session_state["website2_data"]
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

comparison_result = json.loads(ai_text)

st.markdown("---")

st.markdown(
    """
    <h2 style="text-align:center;">
        🤖 AI Comparison Summary
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 📊 Overall Takeaway")

st.markdown(
    f"""
    <div style="
        padding: 18px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #374151;
        line-height: 1.7;
        font-size: 16px;
    ">
        {comparison_result["overall_takeaway"]}
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# MAIN DIFFERENCES
# ------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 🔎 Main Differences")

for difference in comparison_result["main_differences"]:

    st.markdown(
        f"""
        <div style="
            padding: 14px 16px;
            margin-bottom: 10px;
            border-radius: 10px;
            background: #111827;
            border: 1px solid #374151;
            line-height: 1.6;
        ">
            • {difference}
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------
# SECURITY TAKEAWAY
# ------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 🔐 Security Takeaway")

st.markdown(
    f"""
    <div style="
        padding: 18px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #374151;
        line-height: 1.7;
        font-size: 15px;
    ">
        {comparison_result["security_takeaway"]}
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# PRIVACY TAKEAWAY
# ------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 🛡️ Privacy Takeaway")

st.markdown(
    f"""
    <div style="
        padding: 18px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #374151;
        line-height: 1.7;
        font-size: 15px;
    ">
        {comparison_result["privacy_takeaway"]}
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# USER IMPACT
# ------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 👤 What This Means for You")

st.markdown(
    f"""
    <div style="
        padding: 18px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #374151;
        line-height: 1.7;
        font-size: 15px;
    ">
        {comparison_result["user_impact"]}
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# RECOMMENDATION
# ------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 💡 Recommendation")

st.markdown(
    f"""
    <div style="
        padding: 18px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #374151;
        line-height: 1.7;
        font-size: 16px;
    ">
        {comparison_result["recommendation"]}
    </div>
    """,
    unsafe_allow_html=True
)
