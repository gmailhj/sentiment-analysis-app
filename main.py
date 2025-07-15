import streamlit as st
import sidebar
import textPage
import imdbReviewsPage
import imagePage

st.set_page_config(
    page_title="Sentiment Analysis App",
    page_icon="🎭",
    layout="wide"
)

page = sidebar.show()

if page == "Text":
    textPage.renderPage()
elif page == "Movie Analysis":
    imdbReviewsPage.renderPage()
elif page == "Image":
    imagePage.renderPage()
