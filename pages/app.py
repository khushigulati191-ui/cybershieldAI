import streamlit as st
from pages.background import render_background

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
        
st.write(" coming soon")
