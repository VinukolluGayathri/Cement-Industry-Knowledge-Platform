import streamlit as st

from frontend.dashboard import show_dashboard
from frontend.chatbot import show_chatbot
from frontend.upload import show_upload
from frontend.knowledge_graph import show_graph

st.set_page_config(
    page_title="Industrial Knowledge Intelligence Platform",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Industrial Knowledge Intelligence Platform")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Upload Documents",
        "AI Assistant",
        "Knowledge Graph"
    ]
)

if page == "Dashboard":
    show_dashboard()

elif page == "Upload Documents":
    show_upload()

elif page == "AI Assistant":
    show_chatbot()

elif page == "Knowledge Graph":
    show_graph()