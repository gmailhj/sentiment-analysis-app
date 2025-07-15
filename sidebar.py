import streamlit as st
from streamlit_option_menu import option_menu

def show():
    with st.sidebar:
        st.markdown("""
        # Applications
        """, unsafe_allow_html=False)
        
        selected = option_menu(
            menu_title=None,  # required
            options=["Text", "Movie Analysis", "Image"],  # required
            icons=["card-text", "film", "image"],  # optional
            default_index=0,  # optional
        )
        
        return selected
