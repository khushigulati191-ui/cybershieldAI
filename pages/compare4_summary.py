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
from prompts import app_comparison_prompt

load_dotenv()

api_key = os.getenv("api_key")

prompt = app_comparison_prompt.format(
    ios_data=st.session_state["ios_data"],
    android_data=st.session_state["android_data"]
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

import re
response.raise_for_status()

result = response.json()

ai_text = result["choices"][0]["message"]["content"]

ai_text = ai_text.strip()

if ai_text.startswith("```"):
    ai_text = re.sub(r"^```(?:json)?\s*", "", ai_text)
    ai_text = re.sub(r"\s*```$", "", ai_text)

try:
    summary = json.loads(ai_text)

except json.JSONDecodeError:
    st.error("❌ some error occurred. please try again later.")

    st.write("### Raw AI Response")
    st.code(ai_text)

    st.stop()
import streamlit as st
import json

st.subheader("📱 Compare Same App — Android vs iOS")

# =========================
# OVERALL TAKEAWAY
# =========================

st.markdown("### 📌 Overall Takeaway")

st.info(
    summary["overall_takeaway"]
)


# =========================
# BASIC DIFFERENCES
# =========================

st.markdown("### ⚖️ Basic Differences")

for item in summary["basic_differences"]:

    st.markdown(f"#### {item['aspect']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🤖 Android**")
        st.write(item["android"])

    with col2:
        st.markdown("**🍎 iOS**")
        st.write(item["ios"])

    st.markdown(
        f"**Difference:** {item['difference']}"
    )

    st.divider()


# =========================
# IMPORTANT DIFFERENCES
# =========================

st.markdown("### 🚨 Important Differences")

for difference in summary["important_differences"]:
    st.write(f"• {difference}")


# =========================
# ANDROID ADVANTAGES
# =========================

st.markdown("### 🤖 Android Advantages")

for advantage in summary["android_advantages"]:
    st.write(f"• {advantage}")


# =========================
# iOS ADVANTAGES
# =========================

st.markdown("### 🍎 iOS Advantages")

for advantage in summary["ios_advantages"]:
    st.write(f"• {advantage}")


# =========================
# PRIVACY COMPARISON
# =========================

st.markdown("### 🔐 Privacy Comparison")

privacy = summary["privacy_comparison"]

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🤖 Android**")
    st.write(privacy["android"])

with col2:
    st.markdown("**🍎 iOS**")
    st.write(privacy["ios"])

st.markdown(
    f"**Better Privacy:** {privacy['better_privacy']}"
)

st.write(
    f"**Reason:** {privacy['reason']}"
)


# =========================
# SECURITY COMPARISON
# =========================

st.markdown("### 🛡️ Security Comparison")

security = summary["security_comparison"]

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🤖 Android**")
    st.write(security["android"])

with col2:
    st.markdown("**🍎 iOS**")
    st.write(security["ios"])

st.markdown(
    f"**Better Security:** {security['better_security']}"
)

st.write(
    f"**Reason:** {security['reason']}"
)


# =========================
# FINAL RECOMMENDATION
# =========================

st.markdown("### 🎯 Final Recommendation")

recommendation = summary["recommendation"]

if recommendation["decision"] == "ANDROID":

    st.success(
        f"🤖 **Android** — {recommendation['reason']}"
    )

elif recommendation["decision"] == "IOS":

    st.success(
        f"🍎 **iOS** — {recommendation['reason']}"
    )

else:

    st.info(
        f"⚖️ **Similar** — {recommendation['reason']}"
    )