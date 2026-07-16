# comparing two apps on iphone

import streamlit as st
import requests,time
from iphone.get_id import get_ios_app_ids
from iphone.sec_functions import check_developer_verification,check_update_frequency,check_developer_website,check_permissions_transparency
from iphone.priv_functions import analyze_privacy_labels,analyze_privacy_policy, analyze_data_collection,analyze_tracking_indicators
from background import render_background

render_background()

st.title("Iphone App Security & Privacy Comparison")

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

#expanders
st.markdown("""
<style>

div[data-testid="stExpander"] {
    border: 1px solid rgba(0,255,200,0.3) !important;
    border-radius: 18px !important;
    background: rgba(20,25,40,0.7) !important;
    overflow: hidden;
    margin-bottom: 15px;
}

div[data-testid="stExpander"] details summary {
    font-size: 20px !important;
    font-weight: 600 !important;
    padding: 18px !important;
}

div[data-testid="stExpander"] details[open] {
    background: linear-gradient(
        90deg,
        rgba(0,255,200,0.08),
        rgba(0,100,255,0.03)
    );
}

</style>
""", unsafe_allow_html=True)

compare_type = st.session_state.get("compare_type")
os_type = st.session_state.get("os_type")
app1 = st.session_state.get("app1")
app2 = st.session_state.get("app2")


info1 = get_ios_app_ids(app1)
metadata1 = info1["metadata"]
analysis1 = {}

analysis1["developer"] = check_developer_verification(metadata1)
analysis1["frequency"] = check_update_frequency(metadata1)
analysis1["website"] = check_developer_website(metadata1)
analysis1["permission"] = check_permissions_transparency(metadata1)


security_score1 = sum([
    analysis1["developer"]["score"],
    analysis1["frequency"]["score"],
    analysis1["website"]["score"],
    analysis1["permission"]["score"]
])

analysis_priv1 = {}

analysis_priv1["labels"] = analyze_privacy_labels(metadata1)
analysis_priv1["policy"] = analyze_privacy_policy(metadata1)
analysis_priv1["data"] = analyze_data_collection(metadata1)
analysis_priv1["indicators"] = analyze_tracking_indicators(metadata1)

privacy_score1 = sum([
    analysis_priv1["labels"]["score"],
    analysis_priv1["policy"]["score"],
    analysis_priv1["data"]["score"],
    analysis_priv1["indicators"]["score"]
])

info2 = get_ios_app_ids(app2)
metadata2 = info2["metadata"]
analysis2 = {}

analysis2["developer"] = check_developer_verification(metadata2)
analysis2["frequency"] = check_update_frequency(metadata2)
analysis2["website"] = check_developer_website(metadata2)
analysis2["permission"] = check_permissions_transparency(metadata2)


security_score2 = sum([
    analysis2["developer"]["score"],
    analysis2["frequency"]["score"],
    analysis2["website"]["score"],
    analysis2["permission"]["score"]
])

analysis_priv2 = {}

analysis_priv2["labels"] = analyze_privacy_labels(metadata2)
analysis_priv2["policy"] = analyze_privacy_policy(metadata2)
analysis_priv2["data"] = analyze_data_collection(metadata2)
analysis_priv2["indicators"] = analyze_tracking_indicators(metadata2)

privacy_score2 = sum([
    analysis_priv2["labels"]["score"],
    analysis_priv2["policy"]["score"],
    analysis_priv2["data"]["score"],
    analysis_priv2["indicators"]["score"]
])
col1,col2 = st.columns(2)
with col1:
    st.header("Security Analysis")
    st.write(f"{app1} - {os_type}")

    with st.expander(f"Developer Verification : {analysis1["developer"]["verification_score"]}"):
        for k,v in analysis1["developer"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Update Frequency  : {analysis1["frequency"]["update_score"]}"):
        for k,v in analysis1["frequency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Website  : {analysis1["website"]["website_score"]}"):
        for k,v in analysis1["website"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Permissions Transparency  : {analysis1["permission"]["permission_score"]}"):
        for k,v in analysis1["permission"].items():
            st.write(f"{k} : {v}")
    
    st.write(f"""
    Overall Score : {security_score1}/100
""")
    
    if security_score1 >= 80:
        risk = "🟢 Low Risk"
        color = "#00c853"

    elif security_score1 >= 50:
        risk = "🟡 Medium Risk"
        color = "#f5b31a"

    else:
        risk = "🔴 High Risk"
        color = "#f41e1e"

    st.markdown(f"""
    <div style="
        background:{color};
        padding:18px;
        border-radius:15px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        color:white;
        margin-top:20px;">
        {risk}
    </div><br>
    """, unsafe_allow_html=True)

    st.header("Privacy Analysis")
    with st.expander(f"Privacy Label Score : {analysis_priv1["labels"]["label score"]}"):
        for k,v in analysis_priv1["labels"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Privacy Policy Score : {analysis_priv1["policy"]["policy score"]}"):
        for k,v in analysis_priv1["policy"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Data Collection Score : {analysis_priv1["data"]["indicator score"]}"):
        for k,v in analysis_priv1["data"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Tracking Indicator Score : {analysis_priv1["indicators"]["tracking indicator"]}"):
        for k,v in analysis_priv1["indicators"].items():
            st.write(f"{k} : {v}")
    
    st.write(f"""
    Overall Score : {privacy_score1}/100
""")

    if privacy_score1 >= 80:
        risk = "🟢 Low Risk"
        color = "#00c853"

    elif privacy_score1 >= 50:
        risk = "🟡 Medium Risk"
        color = "#f5b31a"

    else:
        risk = "🔴 High Risk"
        color = "#f41e1e"

    st.markdown(f"""
    <div style="
        background:{color};
        padding:18px;
        border-radius:15px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        color:white;
        margin-top:20px;">
        {risk}
    </div><br>
    """, unsafe_allow_html=True)


with col2:
    st.header("Security Analysis")
    st.write(f"{app2} - {os_type}")

    with st.expander(f"Developer Verification : {analysis2["developer"]["verification_score"]}"):
        for k,v in analysis2["developer"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Update Frequency  : {analysis2["frequency"]["update_score"]}"):
        for k,v in analysis2["frequency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Website  : {analysis2["website"]["website_score"]}"):
        for k,v in analysis2["website"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Permissions Transparency  : {analysis2["permission"]["permission_score"]}"):
        for k,v in analysis2["permission"].items():
            st.write(f"{k} : {v}")
    
    st.write(f"""
    Overall Score : {security_score2}/100
""")
    

    if security_score2 >= 80:
        risk = "🟢 Low Risk"
        color = "#00c853"

    elif security_score2 >= 50:
        risk = "🟡 Medium Risk"
        color = "#f5b31a"

    else:
        risk = "🔴 High Risk"
        color = "#f41e1e"

    st.markdown(f"""
    <div style="
        background:{color};
        padding:18px;
        border-radius:15px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        color:white;
        margin-top:20px;">
        {risk}
    </div><br>
    """, unsafe_allow_html=True)

    st.header("Privacy Analysis")
    with st.expander(f"Privacy Label Score : {analysis_priv2["labels"]["label score"]}"):
        for k,v in analysis_priv2["labels"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Privacy Policy Score : {analysis_priv2["policy"]["policy score"]}"):
        for k,v in analysis_priv2["policy"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Data Collection Score : {analysis_priv2["data"]["indicator score"]}"):
        for k,v in analysis_priv2["data"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Tracking Indicator Score : {analysis_priv2["indicators"]["tracking indicator"]}"):
        for k,v in analysis_priv2["indicators"].items():
            st.write(f"{k} : {v}")
    
    st.write(f"""
    Overall Score : {privacy_score2}/100
""")

    if privacy_score2 >= 80:
        risk = "🟢 Low Risk"
        color = "#00c853"

    elif privacy_score2 >= 50:
        risk = "🟡 Medium Risk"
        color = "#f5b31a"

    else:
        risk = "🔴 High Risk"
        color = "#f41e1e"

    st.markdown(f"""
    <div style="
        background:{color};
        padding:18px;
        border-radius:15px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
        color:white;
        margin-top:20px;">
        {risk}
    </div><br>
    """, unsafe_allow_html=True)