import streamlit as st
import requests,time

# BACKGROUND
# st.markdown("""
# <style>

# [data-testid="stAppViewContainer"] {

# background-color:#0B1120;

# background-image:

# linear-gradient(
# rgba(0,255,255,0.15) 2px,
# transparent 2px
# ),

# linear-gradient(
# 90deg,
# rgba(0,255,255,0.15) 2px,
# transparent 2px
# ),

# radial-gradient(
# circle at center,
# rgba(37,99,235,0.25),
# transparent 70%
# );

# background-size:
# 60px 60px,
# 60px 60px,
# 100% 100%;
# }

# </style>
# """, unsafe_allow_html=True)



#TITLE 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;500&display=swap');
</style>
            
<h1 style="
text-align:center;
font-family:'Orbitron';
color:#00FFAA;
font-size:60px;">
🛡️ CyberShield AI
</h1>


<p style="
text-align:center;
font-family:'Poppins';
font-size:20px;
color:white;">
AI-Powered Website Security & Privacy Analysis
</p>
<br>
<br>
<p style="
text-align:center;
font-family:'Poppins';
font-size:20px;
color:white;
margin-top:-20px;">
Analyze any website for security risks, privacy concerns, trackers,  
SSL issues, and trust indicators—all explained by AI in simple language
</p>
""", unsafe_allow_html=True)
st.set_page_config(page_title="CyberShield AI", page_icon="🛡️", layout="wide")

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


#button
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;500&display=swap');
div.stButton > button > div {
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


#body
url = st.text_input(" ", placeholder="Enter Website URL....https://example.com", 
                    help="Enter the full URL of the website you want to analyze, including http:// or https://")

if not url.startswith(("http://", "https://")):
    url = "https://" + url


# -------------------
# Streamlit Layer
# -------------------


if st.button("Analyze Website",type = "tertiary"):
    try:
        with st.spinner("Analyzing website..."):
            response = requests.get(url,allow_redirects=True,)
            final_url = response.url
            time.sleep(2)  # Simulate AI work
            
        st.success("Analysis Complete!")
        time.sleep(2)

        st.session_state["final_url"] = final_url
        st.session_state["url"] = url

        st.switch_page("pages/result.py")
    except Exception as e:
        st.error(f"Please enter a valid website address (e.g., google.com, mit.edu, or https://example.com).")
        
