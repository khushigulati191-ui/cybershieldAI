#comparing two apps on android

import streamlit as st
import requests,time
from android.package import get_package_name
from android.get_info import find_metadata
from android.sec_functions import developer,install_count,community_trust,update_frequency,app_age,sus,transparency
from android.priv_functions import PPAv,PPAn,dev_transparency,ads,category_risk
from background import render_background

render_background()

st.title("Android App Security & Privacy Comparison")

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

package_name1 = get_package_name(app1)
info1 = find_metadata(package_name1)

metadata1 = info1["data"]

analysis1 = {}

analysis1["developer"] = developer(metadata1)
analysis1["count"] = install_count(metadata1)
analysis1["trust"] = community_trust(metadata1)
analysis1["frequency"] = update_frequency(metadata1)
analysis1["app_age"] = app_age(metadata1)
analysis1["sus"] = sus(metadata1)
analysis1["transparency"] = transparency(metadata1)


security_score1 = sum([
    analysis1["developer"]["score"],
    analysis1["frequency"]["score"],
    analysis1["count"]["score"],
    analysis1["trust"]["score"],
    analysis1["app_age"]["score"],
    analysis1["sus"]["score"],
    analysis1["transparency"]["score"]
])

analysis_priv1 = {}

analysis_priv1["PPAv"] = PPAv(metadata1)
analysis_priv1["PPAn"] = PPAn(metadata1)
analysis_priv1["transparency"] = dev_transparency(metadata1)
analysis_priv1["ads"] = ads(metadata1)
analysis_priv1["category_risk"] = category_risk(metadata1)


privacy_score1 = sum([
    analysis_priv1["PPAv"]["score"],
    analysis_priv1["PPAn"]["score"],
    analysis_priv1["transparency"]["score"],
    analysis_priv1["ads"]["score"],
    analysis_priv1["category_risk"]["score"]
])

package_name2 = get_package_name(app2)
info2 = find_metadata(package_name2)

metadata2 = info2["data"]

analysis2 = {}

analysis2["developer"] = developer(metadata2)
analysis2["count"] = install_count(metadata2)
analysis2["trust"] = community_trust(metadata2)
analysis2["frequency"] = update_frequency(metadata2)
analysis2["app_age"] = app_age(metadata2)
analysis2["sus"] = sus(metadata2)
analysis2["transparency"] = transparency(metadata2)


security_score2 = sum([
    analysis2["developer"]["score"],
    analysis2["frequency"]["score"],
    analysis2["count"]["score"],
    analysis2["trust"]["score"],
    analysis2["app_age"]["score"],
    analysis2["sus"]["score"],
    analysis2["transparency"]["score"]
])

analysis_priv2 = {}

analysis_priv2["PPAv"] = PPAv(metadata2)
analysis_priv2["PPAn"] = PPAn(metadata2)
analysis_priv2["transparency"] = dev_transparency(metadata2)
analysis_priv2["ads"] = ads(metadata2)
analysis_priv2["category_risk"] = category_risk(metadata2)


privacy_score2 = sum([
    analysis_priv2["PPAv"]["score"],
    analysis_priv2["PPAn"]["score"],
    analysis_priv2["transparency"]["score"],
    analysis_priv2["ads"]["score"],
    analysis_priv2["category_risk"]["score"]
])



col1,col2 = st.columns(2)
with col1:
    st.header("Security Analysis")
    st.write(f"{app1} - {os_type}")

    with st.expander(f"Developer Verification Score : {analysis1["developer"]["Developer Score"]}"):
        for k,v in analysis1["developer"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Install Count Score : {analysis1["count"]["Install score"]}"):
        for k,v in analysis1["count"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"community Trust Score : {analysis1["trust"]["Community score"]}"):
        for k,v in analysis1["trust"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Update Frequency  : {analysis1["frequency"]["Update Frequency Score"]}"):
        for k,v in analysis1["frequency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"App Age Score  : {analysis1["app_age"]["Age score"]}"):
        for k,v in analysis1["app_age"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Suspicious Keywords Score : {analysis1["sus"]["Sus score"]}"):
        for k,v in analysis1["sus"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Transparency Score : {analysis1["transparency"]["transparency_score"]}"):
        for k,v in analysis1["transparency"].items():
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
    with st.expander(f"Privacy Policy Availability Score : {analysis_priv1["PPAv"]["PPA score"]}"):
        for k,v in analysis_priv1["PPAv"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"privacy Policy Finding Score: {analysis_priv1["PPAn"]["Analysis score"]}"):
        for k,v in analysis_priv1["PPAn"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Transparency Score : {analysis_priv1["transparency"]["transparency score"]}"):
        for k,v in analysis_priv1["transparency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Advertisements Score : {analysis_priv1["ads"]["Ads score"]}"):
        for k,v in analysis_priv1["ads"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Category Risk Score : {analysis_priv1["category_risk"]["category score"]}"):
        for k,v in analysis_priv1["category_risk"].items():
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



with col2:
    st.header("Security Analysis")
    st.write(f"{app2} - {os_type}")

    with st.expander(f"Developer Verification Score : {analysis2["developer"]["Developer Score"]}"):
        for k,v in analysis2["developer"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Install Count Score : {analysis2["count"]["Install score"]}"):
        for k,v in analysis2["count"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"community Trust Score : {analysis2["trust"]["Community score"]}"):
        for k,v in analysis2["trust"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Update Frequency  : {analysis2["frequency"]["Update Frequency Score"]}"):
        for k,v in analysis2["frequency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"App Age Score  : {analysis2["app_age"]["Age score"]}"):
        for k,v in analysis2["app_age"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Suspicious Keywords Score : {analysis2["sus"]["Sus score"]}"):
        for k,v in analysis2["sus"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Transparency Score : {analysis2["transparency"]["transparency_score"]}"):
        for k,v in analysis2["transparency"].items():
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
    with st.expander(f"Privacy Policy Availability Score : {analysis_priv2["PPAv"]["PPA score"]}"):
        for k,v in analysis_priv2["PPAv"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"privacy Policy Finding Score: {analysis_priv2["PPAn"]["Analysis score"]}"):
        for k,v in analysis_priv2["PPAn"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Developer Transparency Score : {analysis_priv2["transparency"]["transparency score"]}"):
        for k,v in analysis_priv2["transparency"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Advertisements Score : {analysis_priv2["ads"]["Ads score"]}"):
        for k,v in analysis_priv2["ads"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Category Risk Score : {analysis_priv2["category_risk"]["category score"]}"):
        for k,v in analysis_priv2["category_risk"].items():
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
