import streamlit as st


def initialize_session():
    if 'logged' not in st.session_state:
        st.session_state.logged = False

    if 'user' not in st.session_state:
        st.session_state.user = None

    if 'username' not in st.session_state:
        st.session_state.username = ""


def reset_session():
    st.session_state.logged = False
    st.session_state.user = None
    st.session_state.username = ""
