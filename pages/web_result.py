import streamlit as st
import requests,time
from website.sec_functions import https_check,ssl_check,domain_check,security_headers_check,indicators_check,DNS_check
from website.priv_functions import cookies_check,third_party_trackers_check,ads_check,privacy_policy_check,data_collection_indicators_check,social_media_trackers_check,detect_cookie_banner
from background import render_background

render_background()

st.title(" Website Security & Privacy Analysis")

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
final_url = st.session_state.get("final_url")
url = st.session_state.get("url")


analysis = {}

analysis["https"] = https_check(final_url)
analysis["ssl"] = ssl_check(final_url)
analysis["domain"] = domain_check(final_url)
analysis["headers"] = security_headers_check(final_url)
analysis["indicators"] = indicators_check(final_url,url)
analysis["dns"] = DNS_check(final_url)


security_score = sum([
    analysis["https"]["score"],
    analysis["ssl"]["score"],
    analysis["domain"]["score"],
    analysis["headers"]["score"],
    analysis["indicators"]["score"],
    analysis["dns"]["score"],

])

analysis_priv = {}

analysis_priv["cookies"] = cookies_check(final_url)
analysis_priv["TPT"] = third_party_trackers_check(final_url)
analysis_priv["ADS"] = ads_check(final_url)
analysis_priv["PPC"] = privacy_policy_check(final_url)
analysis_priv["DCI"] = data_collection_indicators_check(final_url)
analysis_priv["SMT"] = social_media_trackers_check(final_url)
analysis_priv["CB"] = detect_cookie_banner(final_url)

privacy_score = sum([
    analysis_priv["cookies"]["score"],
    analysis_priv["TPT"]["score"],
    analysis_priv["ADS"]["score"],
    analysis_priv["PPC"]["score"],
    analysis_priv["DCI"]["score"],
    analysis_priv["SMT"]["score"],
    analysis_priv["CB"]["score"]
])

st.write(f"{final_url}")


col1,col2 = st.columns(2)
with col1:
    st.header("Security Analysis")
    with st.expander(f"HTTPS Security : {analysis["https"]["https_score"]}"):
        for k,v in analysis["https"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"SSL  : {analysis["ssl"]["ssl_score"]}"):
        for k,v in analysis["ssl"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Domain check  : {analysis["domain"]["domain_score"]}"):
        for k,v in analysis["domain"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Headers check  : {analysis["headers"]["security_header_score"]}"):
        for k,v in analysis["headers"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Indicators check  : {analysis["indicators"]["indicators_score"]}"):
        for k,v in analysis["indicators"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"DNS check  : {analysis["dns"]["DNS_score"]}"):
        for k,v in analysis["dns"].items():
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
    with st.expander(f"Cookie score : {analysis_priv["cookies"]["Cookies_score"]}"):
        for k,v in analysis_priv["cookies"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"TPT score : {analysis_priv["TPT"]["TPT_score"]}"):
        for k,v in analysis_priv["TPT"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"ADS score : {analysis_priv["ADS"]["ADS_score"]}"):
        for k,v in analysis_priv["ADS"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Privacy Policy score : {analysis_priv["PPC"]["PPC_score"]}"):
        for k,v in analysis_priv["PPC"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Data Collection Indicators score : {analysis_priv["DCI"]["data_collection_indicators_score"]}"):
        for k,v in analysis_priv["DCI"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Social Media Trackers score : {analysis_priv["SMT"]["SMT_score"]}"):
        for k,v in analysis_priv["SMT"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Consent Banner score : {analysis_priv["CB"]["CB_score"]}"):
        for k,v in analysis_priv["CB"].items():
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

