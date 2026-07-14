import streamlit as st
from background import render_background
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


#streamlit margins
st.markdown("""
<style>
.block-container {
    padding-bottom: 1rem !important;
}
</style>
""", unsafe_allow_html=True)


# ================= CSS =================
st.markdown("""
<style>

.about-title{
    font-size:48px;
    font-weight:700;
    color:#00F5D4;
    text-align:center;
    font-family:'Orbitron', sans-serif;
    margin-top:20px;
    margin-bottom:10px;
    text-shadow:0 0 15px rgba(0,245,212,0.7);
}

.about-subtitle{
    text-align:center;
    color:#A0AEC0;
    font-size:18px;
    margin-bottom:50px;
}

.cyber-card{
    background:rgba(17,25,40,0.75);
    border:1px solid rgba(0,245,212,0.2);
    border-radius:20px;
    padding:25px;
    margin-bottom:25px;
    backdrop-filter:blur(10px);
    box-shadow:0 0 20px rgba(0,245,212,0.1);
}

.card-heading{
    color:#00F5D4;
    font-size:28px;
    font-weight:600;
    margin-bottom:20px;
    font-family:'Orbitron', sans-serif;
}

.card-text{
    color:#D1D5DB;
    font-size:17px;
    line-height:1.9;
}

.feature-box{
    background:rgba(0,245,212,0.06);
    border:1px solid rgba(0,245,212,0.15);
    border-radius:15px;
    padding:20px;
    text-align:center;
    height:250px;
    transition:0.3s;
}

.feature-box:hover{
    transform:translateY(-5px);
    box-shadow:0 0 20px rgba(0,245,212,0.25);
}

.feature-title{
    color:#00F5D4;
    font-size:20px;
    font-weight:600;
    margin-bottom:15px;
}

.feature-text{
    color:#D1D5DB;
    font-size:15px;
}

.goal-box{
    text-align:center;
    color:#D1D5DB;
    font-size:18px;
    line-height:1.8;
}

.tech{
    color:#00F5D4;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)


# ================= Title =================
st.markdown(
    '<div class="about-title">About CyberShield AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="about-subtitle">'
    'AI-Powered Website Security & Privacy Analysis Platform'
    '</div>',
    unsafe_allow_html=True
)

# ================= Overview =================
st.markdown("""
<div class="cyber-card">
<div class="card-heading">🛡️ Project Overview</div>

<div class="card-text">

<b>CyberShield AI</b> is an AI-driven cybersecurity platform designed to help users
understand whether a website is secure, trustworthy, and respectful of user privacy.

The platform automatically analyzes publicly available information and transforms
technical findings into simple, easy-to-understand insights.

Whether you are a student, researcher, professional, or everyday internet user,
CyberShield AI helps you make safer decisions online by identifying potential
security risks and privacy concerns before you interact with a website.

</div>
</div>
""", unsafe_allow_html=True)


# ================= Features =================
st.markdown(
    '<div class="card-heading" style="text-align:center;">Core Features</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">🔒 Security Analysis</div>
        <div class="feature-text">
        • HTTPS Verification<br><br>
        • SSL Certificate Validation<br><br>
        • Security Headers Inspection<br><br>
        • Domain Intelligence & Risk Scoring
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""       
    <div class="feature-box">
        <div class="feature-title">🔍 Privacy Scanner</div>
        <div class="feature-text">
        • Cookie Detection<br><br>
        • Third-Party Tracker Analysis<br><br>
        • Data Collection Indicators<br><br>
        • Privacy Risk Assessment
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">🤖 AI Insights</div>
        <div class="feature-text">
        • Beginner-Friendly Explanations<br><br>
        • Risk Summaries<br><br>
        • Personalized Recommendations<br><br>
        • Simplified Security Reports
        </div>
    </div>
    """, unsafe_allow_html=True)


# ================= Mission =================
st.markdown("""
            <br>
            <br>
<div class="cyber-card">
<div class="card-heading">🎯 Mission</div>

<div class="goal-box">

Our mission is to make cybersecurity and online privacy understandable for everyone.

CyberShield AI bridges the gap between complex security concepts and everyday users
by converting technical website data into clear, actionable insights that empower
people to browse the internet safely and confidently.

</div>
</div>
""", unsafe_allow_html=True)




# ================= Footer =================
st.markdown("""
<div style='text-align:center;
            color:#718096;
            margin-top:60px;
            margin-bottom:0px;
            font-size:15px;'>

Empowering safer browsing through AI-driven security and privacy insights.
</div>
""", unsafe_allow_html=True)