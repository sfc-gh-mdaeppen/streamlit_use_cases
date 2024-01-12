import streamlit as st

st.set_page_config(
    page_title="Welcome Page",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Banks are the gateway to financial services products, and the challenge is to create long-term customer value
    and retention. You can do this through different use cases.
    
    **👈 Select a demo from the sidebar**
"""
)