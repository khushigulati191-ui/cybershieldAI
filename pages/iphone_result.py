import streamlit as st
import requests,time
from iphone.get_id import get_ios_app_ids
from iphone.sec_functions import check_developer_verification,check_update_frequency,check_developer_website,check_permissions_transparency
from iphone.priv_functions import analyze_privacy_labels,analyze_privacy_policy, analyze_data_collection,analyze_tracking_indicators
from background import render_background

render_background()

st.title("Iphone App Security & Privacy Analysis")

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

#content
app_name = st.session_state.get("app_name")
os_type = st.session_state.get("os_type")

info = get_ios_app_ids(app_name)
metadata = info["metadata"]
analysis = {}

analysis["developer"] = check_developer_verification(metadata)
analysis["frequency"] = check_update_frequency(metadata)
analysis["website"] = check_developer_website(metadata)
analysis["permission"] = check_permissions_transparency(metadata)


security_score = sum([
    analysis["developer"]["score"],
    analysis["frequency"]["score"],
    analysis["website"]["score"],
    analysis["permission"]["score"]
])

analysis_priv = {}

analysis_priv["labels"] = analyze_privacy_labels(metadata)
analysis_priv["policy"] = analyze_privacy_policy(metadata)
analysis_priv["data"] = analyze_data_collection(metadata)
analysis_priv["indicators"] = analyze_tracking_indicators(metadata)

privacy_score = sum([
    analysis_priv["labels"]["score"],
    analysis_priv["policy"]["score"],
    analysis_priv["data"]["score"],
    analysis_priv["indicators"]["score"]
])

st.write(f"{app_name} - {os_type}")


col1,col2 = st.columns(2)
with col1:
    st.header("Security Analysis")
    with st.expander(f"Developer Verification : {analysis["developer"]["verification_score"]}"):
        for k,v in analysis["developer"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Update Frequency  : {analysis["frequency"]["update_score"]}"):
        for k,v in analysis["frequency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Website  : {analysis["website"]["website_score"]}"):
        for k,v in analysis["website"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Permissions Transparency  : {analysis["permission"]["permission_score"]}"):
        for k,v in analysis["permission"].items():
            st.write(f"{k} : {v}")
    
    st.write(f"""
    Overall Score : {security_score}/100
""")
    

    if security_score >= 80:
        risk = "🟢 Low Risk"
        color = "#00c853"

    elif security_score >= 50:
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
    st.header("Privacy Analysis")
    with st.expander(f"Privacy Label Score : {analysis_priv["labels"]["label score"]}"):
        for k,v in analysis_priv["labels"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Privacy Policy Score : {analysis_priv["policy"]["policy score"]}"):
        for k,v in analysis_priv["policy"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Data Collection Score : {analysis_priv["data"]["indicator score"]}"):
        for k,v in analysis_priv["data"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Tracking Indicator Score : {analysis_priv["indicators"]["tracking indicator"]}"):
        for k,v in analysis_priv["indicators"].items():
            st.write(f"{k} : {v}")
    
    st.write(f"""
    Overall Score : {privacy_score}/100
""")

    if privacy_score >= 80:
        risk = "🟢 Low Risk"
        color = "#00c853"

    elif privacy_score >= 50:
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

st.markdown(
    """
    <style>
    div.stButton {
        text-align: center;
    }
    </style>
    """, 
    unsafe_allow_html=True
    )

if st.button("Get in depth analysis"):
    st.switch_page("pages/details.py")


