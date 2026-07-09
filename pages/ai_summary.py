import streamlit as st
from pages.background import render_background

render_background()

st.write("summary coming soon")
if st.button("GET DEPTH ANALYSIS", type = "tertiary"):
    
    st.switch_page("pages/result.py")