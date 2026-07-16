#comparing two websites

import streamlit as st
import requests,time
from website.sec_functions import https_check,ssl_check,domain_check,security_headers_check,indicators_check,DNS_check
from website.priv_functions import cookies_check,third_party_trackers_check,ads_check,privacy_policy_check,data_collection_indicators_check,social_media_trackers_check,detect_cookie_banner
from background import render_background

render_background()

st.title(" Website Security & Privacy Comparison")

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

url1 = st.session_state.get("url1")
url2 = st.session_state.get("url2")
final_url1 = st.session_state.get("final_url1")
final_url2 = st.session_state.get("final_url2")

analysis1 = {}

analysis1["https"] = https_check(final_url1)
analysis1["ssl"] = ssl_check(final_url1)
analysis1["domain"] = domain_check(final_url1)
analysis1["headers"] = security_headers_check(final_url1)
analysis1["indicators"] = indicators_check(final_url1,url1)
analysis1["dns"] = DNS_check(final_url1)


security_score1 = sum([
    analysis1["https"]["score"],
    analysis1["ssl"]["score"],
    analysis1["domain"]["score"],
    analysis1["headers"]["score"],
    analysis1["indicators"]["score"],
    analysis1["dns"]["score"],

])

analysis_priv1 = {}

analysis_priv1["cookies"] = cookies_check(final_url1)
analysis_priv1["TPT"] = third_party_trackers_check(final_url1)
analysis_priv1["ADS"] = ads_check(final_url1)
analysis_priv1["PPC"] = privacy_policy_check(final_url1)
analysis_priv1["DCI"] = data_collection_indicators_check(final_url1)
analysis_priv1["SMT"] = social_media_trackers_check(final_url1)
analysis_priv1["CB"] = detect_cookie_banner(final_url1)

privacy_score1 = sum([
    analysis_priv1["cookies"]["score"],
    analysis_priv1["TPT"]["score"],
    analysis_priv1["ADS"]["score"],
    analysis_priv1["PPC"]["score"],
    analysis_priv1["DCI"]["score"],
    analysis_priv1["SMT"]["score"],
    analysis_priv1["CB"]["score"]
])

analysis2 = {}

analysis2["https"] = https_check(final_url2)
analysis2["ssl"] = ssl_check(final_url2)
analysis2["domain"] = domain_check(final_url2)
analysis2["headers"] = security_headers_check(final_url2)
analysis2["indicators"] = indicators_check(final_url2,url2)
analysis2["dns"] = DNS_check(final_url2)


security_score2 = sum([
    analysis2["https"]["score"],
    analysis2["ssl"]["score"],
    analysis2["domain"]["score"],
    analysis2["headers"]["score"],
    analysis2["indicators"]["score"],
    analysis2["dns"]["score"],

])

analysis_priv2 = {}

analysis_priv2["cookies"] = cookies_check(final_url2)
analysis_priv2["TPT"] = third_party_trackers_check(final_url2)
analysis_priv2["ADS"] = ads_check(final_url2)
analysis_priv2["PPC"] = privacy_policy_check(final_url2)
analysis_priv2["DCI"] = data_collection_indicators_check(final_url2)
analysis_priv2["SMT"] = social_media_trackers_check(final_url2)
analysis_priv2["CB"] = detect_cookie_banner(final_url2)

privacy_score2 = sum([
    analysis_priv2["cookies"]["score"],
    analysis_priv2["TPT"]["score"],
    analysis_priv2["ADS"]["score"],
    analysis_priv2["PPC"]["score"],
    analysis_priv2["DCI"]["score"],
    analysis_priv2["SMT"]["score"],
    analysis_priv2["CB"]["score"]
])


col1,col2 = st.columns(2)
with col1:
    st.header("Security Analysis")
    st.write(f"{final_url1}")

    with st.expander(f"HTTPS Security : {analysis1["https"]["https_score"]}"):
        for k,v in analysis1["https"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"SSL  : {analysis1["ssl"]["ssl_score"]}"):
        for k,v in analysis1["ssl"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Domain check  : {analysis1["domain"]["domain_score"]}"):
        for k,v in analysis1["domain"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Headers check  : {analysis1["headers"]["security_header_score"]}"):
        for k,v in analysis1["headers"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Indicators check  : {analysis1["indicators"]["indicators_score"]}"):
        for k,v in analysis1["indicators"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"DNS check  : {analysis1["dns"]["DNS_score"]}"):
        for k,v in analysis1["dns"].items():
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
    with st.expander(f"Cookie score : {analysis_priv1["cookies"]["Cookies_score"]}"):
        for k,v in analysis_priv1["cookies"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"TPT score : {analysis_priv1["TPT"]["TPT_score"]}"):
        for k,v in analysis_priv1["TPT"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"ADS score : {analysis_priv1["ADS"]["ADS_score"]}"):
        for k,v in analysis_priv1["ADS"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Privacy Policy score : {analysis_priv1["PPC"]["PPC_score"]}"):
        for k,v in analysis_priv1["PPC"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Data Collection Indicators score : {analysis_priv1["DCI"]["data_collection_indicators_score"]}"):
        for k,v in analysis_priv1["DCI"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Social Media Trackers score : {analysis_priv1["SMT"]["SMT_score"]}"):
        for k,v in analysis_priv1["SMT"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Consent Banner score : {analysis_priv1["CB"]["CB_score"]}"):
        for k,v in analysis_priv1["CB"].items():
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
    st.write(f"{final_url2}")

    with st.expander(f"HTTPS Security : {analysis2["https"]["https_score"]}"):
        for k,v in analysis2["https"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"SSL  : {analysis2["ssl"]["ssl_score"]}"):
        for k,v in analysis2["ssl"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Domain check  : {analysis2["domain"]["domain_score"]}"):
        for k,v in analysis2["domain"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Headers check  : {analysis2["headers"]["security_header_score"]}"):
        for k,v in analysis2["headers"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Indicators check  : {analysis2["indicators"]["indicators_score"]}"):
        for k,v in analysis2["indicators"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"DNS check  : {analysis2["dns"]["DNS_score"]}"):
        for k,v in analysis2["dns"].items():
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
    with st.expander(f"Cookie score : {analysis_priv2["cookies"]["Cookies_score"]}"):
        for k,v in analysis_priv2["cookies"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"TPT score : {analysis_priv2["TPT"]["TPT_score"]}"):
        for k,v in analysis_priv2["TPT"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"ADS score : {analysis_priv2["ADS"]["ADS_score"]}"):
        for k,v in analysis_priv2["ADS"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Privacy Policy score : {analysis_priv2["PPC"]["PPC_score"]}"):
        for k,v in analysis_priv2["PPC"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Data Collection Indicators score : {analysis_priv2["DCI"]["data_collection_indicators_score"]}"):
        for k,v in analysis_priv2["DCI"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Social Media Trackers score : {analysis_priv2["SMT"]["SMT_score"]}"):
        for k,v in analysis_priv2["SMT"].items():
            st.write(f"{k} : {v}")
    with st.expander(f"Consent Banner score : {analysis_priv2["CB"]["CB_score"]}"):
        for k,v in analysis_priv2["CB"].items():
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
