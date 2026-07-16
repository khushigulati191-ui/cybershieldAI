import streamlit as st
import requests,time
from android.package import get_package_name
from android.get_info import find_metadata
from android.sec_functions import developer,install_count,community_trust,update_frequency,app_age,sus,transparency
from android.priv_functions import PPAv,PPAn,dev_transparency,ads,category_risk
from background import render_background

render_background()

st.title("Android App Security & Privacy Analysis")

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

package_name = get_package_name(app_name)
info = find_metadata(package_name)

metadata = info["data"]

analysis = {}

analysis["developer"] = developer(metadata)
analysis["count"] = install_count(metadata)
analysis["trust"] = community_trust(metadata)
analysis["frequency"] = update_frequency(metadata)
analysis["app_age"] = app_age(metadata)
analysis["sus"] = sus(metadata)
analysis["transparency"] = transparency(metadata)


security_score = sum([
    analysis["developer"]["score"],
    analysis["frequency"]["score"],
    analysis["count"]["score"],
    analysis["trust"]["score"],
    analysis["app_age"]["score"],
    analysis["sus"]["score"],
    analysis["transparency"]["score"]
])

analysis_priv = {}

analysis_priv["PPAv"] = PPAv(metadata)
analysis_priv["PPAn"] = PPAn(metadata)
analysis_priv["transparency"] = dev_transparency(metadata)
analysis_priv["ads"] = ads(metadata)
analysis_priv["category_risk"] = category_risk(metadata)


privacy_score = sum([
    analysis_priv["PPAv"]["score"],
    analysis_priv["PPAn"]["score"],
    analysis_priv["transparency"]["score"],
    analysis_priv["ads"]["score"],
    analysis_priv["category_risk"]["score"]
])

st.write(f"{app_name} - {os_type}")


col1,col2 = st.columns(2)
with col1:
    st.header("Security Analysis")
    with st.expander(f"Developer Verification Score : {analysis["developer"]["Developer Score"]}"):
        for k,v in analysis["developer"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Install Count Score : {analysis["count"]["Install score"]}"):
        for k,v in analysis["count"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"community Trust Score : {analysis["trust"]["Community score"]}"):
        for k,v in analysis["trust"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Update Frequency  : {analysis["frequency"]["Update Frequency Score"]}"):
        for k,v in analysis["frequency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"App Age Score  : {analysis["app_age"]["Age score"]}"):
        for k,v in analysis["app_age"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Suspicious Keywords Score : {analysis["sus"]["Sus score"]}"):
        for k,v in analysis["sus"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Transparency Score : {analysis["transparency"]["transparency_score"]}"):
        for k,v in analysis["transparency"].items():
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
    with st.expander(f"Privacy Policy Availability Score : {analysis_priv["PPAv"]["PPA score"]}"):
        for k,v in analysis_priv["PPAv"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"privacy Policy Finding Score: {analysis_priv["PPAn"]["Analysis score"]}"):
        for k,v in analysis_priv["PPAn"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Transparency Score : {analysis_priv["transparency"]["transparency score"]}"):
        for k,v in analysis_priv["transparency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Advertisements Score : {analysis_priv["ads"]["Ads score"]}"):
        for k,v in analysis_priv["ads"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Category Risk Score : {analysis_priv["category_risk"]["category score"]}"):
        for k,v in analysis_priv["category_risk"].items():
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

