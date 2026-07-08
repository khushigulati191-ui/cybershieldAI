import streamlit as st
st.markdown("""
<style>
.test-dot{
    width:20px;
    height:20px;
    border-radius:50%;
    background:#00FFAA;
    animation: blink 1s infinite;
}

@keyframes blink{
    0%,100%{opacity:1;}
    50%{opacity:0.2;}
}
</style>

<div class="test-dot"></div>
""", unsafe_allow_html=True)