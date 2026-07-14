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

st.write("summary coming soon")
if st.button("GET DEPTH ANALYSIS", type = "tertiary"):
    
    st.switch_page("pages/iphone_result.py")