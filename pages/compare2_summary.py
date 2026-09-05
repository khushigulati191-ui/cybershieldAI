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
from prompts import ios_compare_prompt

load_dotenv()

api_key = os.getenv("api_key")

prompt = ios_compare_prompt.format(
    app1_data=st.session_state["app1_data"],
    app2_data=st.session_state["app2_data"]
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

# =========================
# IPHONE APP COMPARISON
# =========================

app1_name = summary["app1_name"]
app2_name = summary["app2_name"]

st.subheader(f"📱 Comparing {app1_name} vs {app2_name}")


# =========================
# OVERALL COMPARISON
# =========================

st.subheader("🔍 Overall Comparison")

st.write(summary["overall_takeaway"])


# =========================
# OVERALL WINNER
# =========================

st.subheader("🏆 Overall Takeaway")

winner = summary["winner"]

winner_app = winner["app"]
winner_reason = winner["reason"]

if winner_app == "Tie":
    st.info("⚖️ Both apps have a similar overall security and privacy posture.")

elif winner_app == "Cannot Determine":
    st.warning("🟡 No clear winner could be determined from the available information.")

elif winner_app == "Neither":
    st.warning("🟡 Neither app can be recommended as clearly better based on the available information.")

else:
    st.success(f"🟢 Better Overall Choice: {winner_app}")

st.write(winner_reason)


# =========================
# SCORE COMPARISON
# =========================

st.subheader("📊 Score Comparison")

scores = summary["score_comparison"]

col1, col2 = st.columns(2)


# =========================
# APP 1 SCORES
# =========================

with col1:

    st.markdown(f"### 📱 {app1_name}")

    app1_security = scores["app1_security_score"]
    app1_privacy = scores["app1_privacy_score"]
    app1_overall = scores["app1_overall_score"]

    if app1_security is not None:
        st.metric(
            label="🔐 Security",
            value=f"{app1_security}/100"
        )

    else:
        st.metric(
            label="🔐 Security",
            value="N/A"
        )

    if app1_privacy is not None:
        st.metric(
            label="🔒 Privacy",
            value=f"{app1_privacy}/100"
        )

    else:
        st.metric(
            label="🔒 Privacy",
            value="N/A"
        )

    if app1_overall is not None:
        st.metric(
            label="🛡️ Overall",
            value=f"{app1_overall}/100"
        )

    else:
        st.metric(
            label="🛡️ Overall",
            value="N/A"
        )


# =========================
# APP 2 SCORES
# =========================

with col2:

    st.markdown(f"### 📱 {app2_name}")

    app2_security = scores["app2_security_score"]
    app2_privacy = scores["app2_privacy_score"]
    app2_overall = scores["app2_overall_score"]

    if app2_security is not None:
        st.metric(
            label="🔐 Security",
            value=f"{app2_security}/100"
        )

    else:
        st.metric(
            label="🔐 Security",
            value="N/A"
        )

    if app2_privacy is not None:
        st.metric(
            label="🔒 Privacy",
            value=f"{app2_privacy}/100"
        )

    else:
        st.metric(
            label="🔒 Privacy",
            value="N/A"
        )

    if app2_overall is not None:
        st.metric(
            label="🛡️ Overall",
            value=f"{app2_overall}/100"
        )

    else:
        st.metric(
            label="🛡️ Overall",
            value="N/A"
        )


# =========================
# SECURITY & PRIVACY ASSESSMENT
# =========================

st.subheader("🛡️ Security & Privacy Assessment")

categories = summary["category_comparison"]


# =========================
# EACH CATEGORY
# =========================

for category in categories:

    category_name = category["category"]

    app1_result = category["app1_result"]
    app2_result = category["app2_result"]

    better_app = category["better_app"]
    explanation = category["explanation"]

    st.markdown(f"### {category_name}")

    col1, col2, col3 = st.columns(3)


    # =========================
    # APP 1
    # =========================

    with col1:

        if app1_result == "Good":
            st.success(
                f"🟢 {app1_name}\n\n"
                f"**{app1_result}**"
            )

        elif app1_result == "Warning":
            st.warning(
                f"🟡 {app1_name}\n\n"
                f"**{app1_result}**"
            )

        elif app1_result == "Risk":
            st.error(
                f"🔴 {app1_name}\n\n"
                f"**{app1_result}**"
            )

        else:
            st.info(
                f"⚪ {app1_name}\n\n"
                f"**{app1_result}**"
            )


    # =========================
    # APP 2
    # =========================

    with col2:

        if app2_result == "Good":
            st.success(
                f"🟢 {app2_name}\n\n"
                f"**{app2_result}**"
            )

        elif app2_result == "Warning":
            st.warning(
                f"🟡 {app2_name}\n\n"
                f"**{app2_result}**"
            )

        elif app2_result == "Risk":
            st.error(
                f"🔴 {app2_name}\n\n"
                f"**{app2_result}**"
            )

        else:
            st.info(
                f"⚪ {app2_name}\n\n"
                f"**{app2_result}**"
            )


    # =========================
    # BETTER APP
    # =========================

    with col3:

        if better_app == "Tie":

            st.info(
                "⚖️ **Both are similar**"
            )

        elif better_app == "Cannot Determine":

            st.info(
                "⚪ **Cannot determine**"
            )

        else:

            st.success(
                f"🏆 **Better: {better_app}**"
            )

    st.write(explanation)


# =========================
# KEY DIFFERENCES
# =========================

st.subheader("🔎 Key Differences")

for finding in summary["key_differences"]:

    title = finding["title"]

    app1_finding = finding["app1"]
    app2_finding = finding["app2"]

    explanation = finding["explanation"]

    with st.expander(title):

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(f"**📱 {app1_name}**")

            st.write(app1_finding)

        with col2:

            st.markdown(f"**📱 {app2_name}**")

            st.write(app2_finding)

        st.markdown("**What this means:**")

        st.write(explanation)


# =========================
# RECOMMENDATION
# =========================

st.subheader("💡 Recommendation")

recommendation = summary["recommendation"]

recommended_app = recommendation["app"]
recommendation_reason = recommendation["reason"]

if recommended_app == "Both":

    st.success(
        "🟢 **Both apps are reasonable choices based on the available information.**"
    )

elif recommended_app == "Neither":

    st.error(
        "🔴 **Neither app can be clearly recommended based on the available information.**"
    )

elif recommended_app == "Cannot Determine":

    st.warning(
        "🟡 **A clear recommendation cannot be made from the available information.**"
    )

else:

    st.success(
        f"🟢 **Recommended App: {recommended_app}**"
    )

st.write(recommendation_reason)