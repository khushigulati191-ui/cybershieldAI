import streamlit as st
import requests,time
from pages.background import render_background


render_background()

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
div[class*="st-key-nav_"] button[type="primary"] {
    color: var(--text-primary) !important;
    background: rgba(34, 211, 238, 0.12) !important;
    border-radius: 8px !important;
    border: 1px solid #00FFAA !important;
}
</style>
""", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "home"


col1, col2, col3, col4 = st.columns([5, 1, 1, 1])


with col2:
    if st.button(
        "Home",
        key="home_btn",
        use_container_width=True,
    ):
        st.session_state.page = "home"
        
        st.rerun()
    if st.session_state.page == "home":
        st.markdown(
            "<div style='height:3px; background:#00E5FF; border-radius:5px; margin-top:4px;'></div>",
            unsafe_allow_html=True
        )

with col3:
    if st.button(
        "Compare",
        key="compare_btn",
        use_container_width=True,
    ):
        st.session_state.page = "compare"
        st.markdown(
            "<div style='height:4px;background:#00E5FF;border-radius:5px;border: 1px solid #00FFAA !important;'></div>",
            unsafe_allow_html=True
        )
        st.switch_page("pages/compare.py")
        st.rerun()

with col4:
    if st.button(
        "About",
        key="about_btn",
        use_container_width=True,
    ):
        st.session_state.page = "about"
        st.markdown(
            "<div style='height:4px;background:#00E5FF;border-radius:5px;border: 1px solid #00FFAA !important;'></div>",
            unsafe_allow_html=True
        )
        st.switch_page("pages/about.py")
        st.rerun()


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




#body

url = st.text_input(" ", placeholder="Enter Website URL....https://example.com", 
                    help="Enter the full URL of the website you want to analyze, or simply type the domain name (e.g., google.com, mit.edu).")

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
        
