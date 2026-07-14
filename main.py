import streamlit as st
import requests,time
from background import render_background
from datetime import datetime, timezone
   


render_background()

st.markdown("""
<style>
.block-container {
    padding-top: 1rem !important;
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



#headers
col1, col2, col3, col4 = st.columns([5, 1, 1, 1])

with col1:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;500&display=swap');
</style>
            
<h1 style="
text-align:left;
font-family:'Orbitron';
color:#00FFAA;
font-size:60px;">
🛡️ CyberShield AI
</h1>

""", unsafe_allow_html=True)

with col3:
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



# remove sidebar
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


st.markdown("""
<style>
.cs-hero{
    text-align:center;
    padding-top:3rem;
    padding-bottom:3rem;
}

/* AI-powered badge */
.cs-eyebrow{
    display:inline-flex;
    align-items:center;
    gap:10px;

    padding:14px 28px;
    border-radius:999px;

    background:rgba(0,20,35,0.65);
    border:1px solid rgba(0,229,255,0.25);

    color:#4DD7FF;
    font-size:20px;
    font-weight:600;
    font-family:monospace;

    box-shadow:0 0 20px rgba(0,229,255,0.1);
}

.cs-eyebrow-dot{
    width:10px;
    height:10px;
    border-radius:50%;
    background:#00FFAA;
    display:inline-block;
    animation: blink 1.5s infinite;
}
@keyframes blink{
    0%,100%{
        opacity:1;
        transform:scale(1);
    }
    50%{
        opacity:0.3;
        transform:scale(1.3);
    }
}
/* Main title */
.cs-hero h1{
    font-size:1.5rem;
    font-weight:800;
    color:#E5E7EB;
    margin-top:2rem;
    margin-bottom:1.5rem;
    line-height:1.1;
}

/* Subtitle */
.cs-hero p{
    font-size:1.5rem;
    color: white ;
    max-width:900px;
    margin:auto;
    line-height:1.7;
    font-text: 'Orbotron', sans-serif;
    padding-top:1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
        f"""
        <div class="cs-hero">
            <div class="cs-eyebrow">
                <span class="cs-eyebrow-dot"></span>
                "AI-Powered Security Intelligence"
            </div>
            
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("""
<style>
<br>            
div[class*="st-key-card_"] {
    background: var(--surface-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 1.7rem 1.5rem 1.5rem 1.5rem;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    height: 100%;
}
div[class*="st-key-card_"]:hover {
    transform: translateY(-4px);
    border-color: var(--border-glass-hover);
    box-shadow: 0 14px 40px rgba(34, 211, 238, 0.14);
}
.cs-card-icon {
    width: 50px; height: 50px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(34, 211, 238, 0.16), rgba(99, 102, 241, 0.16));
    border: 1px solid var(--border-glass);
    color: var(--accent-cyan);
    margin-bottom: 1.1rem;
}
.cs-card-title {
    font-family: var(--font-display);
    font-size: 1.22rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: var(--text-primary);
}
.cs-card-desc {
    font-size: 0.93rem;
    color: var(--text-secondary);
    line-height: 1.55;
    margin-bottom: 1.4rem;
    min-height: 3.3rem;
}
</style>
""", unsafe_allow_html=True)

@st.dialog("Analyze a Website")
def website_popup():
    st.write(
        "Enter a URL and our AI will check it for security, privacy and tracking."
    )

    url = st.text_input(
        "Website URL",
        placeholder="e.g. https://www.example.com"
    )
    if url and not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url  
    
    try:
        if st.button("Analyze Website", use_container_width=True,type = "tertiary"):
            with st.spinner("Analyzing website..."):
                response = requests.get(url,allow_redirects=True,)
                final_url = response.url
                time.sleep(2)  # Simulate AI work
            st.success("Analysis Complete!")
            time.sleep(2)
            st.session_state["final_url"] = final_url
            st.session_state["url"] = url
            st.switch_page("pages/web_ai_summary.py")
    except Exception as e:
        st.error(str(e))
        

@st.dialog("Analyze an App")
def app_popup():
    os_type = st.radio(
        "What are you using?",
        ["Android", "Iphone"],
        horizontal=True,
    )
    app_name = st.text_input(
        "App Name",
        placeholder="e.g. WhatsApp"
    )
    if st.button("Analyze App", use_container_width=True):
        with st.spinner("Analyzing website..."):
                time.sleep(2)  # Simulate AI work
        st.success("Analysis Complete!")
        time.sleep(2)
        st.session_state["os_type"] = os_type
        st.session_state["app_name"] = app_name
        if os_type == "Iphone":
            st.switch_page("pages/iphone_summary.py")
        else:
            st.switch_page("pages/android_summary.py")

    

@st.dialog("Compare Two Services")
def compare_popup():

    st.write("Compare two websites or two apps side-by-side.")

    compare_type = st.radio(
        "What are you comparing?",
        ["Website", "App"],
        horizontal=True,
    )
    if compare_type == "App":
        app_type = st.radio(
        "How do you want to compare?",
        ["Compare two different apps on same operating system-- android/ios", "Compare one app on two operating system-- android and ios"],
        horizontal=True,)   
        if app_type == "Compare two different apps on same operating system-- android/ios":
            col1, col2 = st.columns(2)

            with col1:
                first = st.text_input(
                    "First",
                    placeholder="e.g. Instagram"
                )

            with col2:
                second = st.text_input(
                    "Second",
                    placeholder="e.g. Snapchat")
        else:
            app = st.text_input("App",placeholder = "e.g. Youtube" )
    else:
        col1, col2 = st.columns(2)

        with col1:
            first = st.text_input(
                "First",
                placeholder="e.g. https://instagram.com"
            )

        with col2:
            second = st.text_input(
                "Second",
                placeholder="e.g. https://www.snapchat.com"
            )

    if st.button("Compare", use_container_width=True):

        st.session_state["first"] = first
        st.session_state["second"] = second
        st.switch_page("pages/compare.py")


col1, col2, col3 = st.columns(3,gap = "large")
with col1:
    st.markdown(
        f"""
        <div class="cs-card">
            <div class="cs-card-icon">
                🔒
            </div>
            <h3 class="cs-card-title">Website Analysis</h3>
            <p class="cs-card-desc">Analyze any website for security, privacy, tracking and trustworthiness.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Analyze Website",
        use_container_width=True,):
        website_popup()

        
with col2:
    st.markdown(
        f"""
        <div class="cs-card">
            <div class="cs-card-icon">
                🕵️‍♂️
            </div>
            <h3 class="cs-card-title">Mobile App Analysis</h3>
            <p class="cs-card-desc">Analyze mobile apps for security, privacy, and performance issues.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Analyse App",
        use_container_width=True,):
        app_popup()

with col3:
    st.markdown(
        f"""
        <div class="cs-card">
            <div class="cs-card-icon">
                🤖
            </div>
            <h3 class="cs-card-title">Compare</h3>
            <p class="cs-card-desc">Compare two websites or apps side-by-side using AI.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Compare Now",
        use_container_width=True,):
        compare_popup()


# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;500&display=swap');
# </style>
# <br>
# <br>            
# <h1 style="
# text-align: center;
# font-family: 'Orbitron';
# color: #00FFAA;
# font-size:35px;">
# KNOW BEFORE YOU CLICK
# </h1>

# """, unsafe_allow_html=True)


#body

# url = st.text_input(" ", placeholder="Enter Website URL....https://example.com", 
#                     help="Enter the full URL of the website you want to analyze, or simply type the domain name (e.g., google.com, mit.edu).")

# if not url.startswith(("http://", "https://")):
#     url = "https://" + url


# -------------------
# Streamlit Layer
# -------------------







# if st.button("Analyze Website",type = "tertiary"):
#     try:
#         with st.spinner("Analyzing website..."):
#             response = requests.get(url,allow_redirects=True,)
#             final_url = response.url
#             time.sleep(2)  # Simulate AI work
            
#         st.success("Analysis Complete!")
#         time.sleep(2)

#         st.session_state["final_url"] = final_url
#         st.session_state["url"] = url

#         st.switch_page("pages/result.py")
#     except Exception as e:
#         st.error(f"Please enter a valid website address (e.g., google.com, mit.edu, or https://example.com).")
        
