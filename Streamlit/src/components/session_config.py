import streamlit as st


def initialize_session():
    if 'logged' not in st.session_state:
        st.session_state.logged = False

    if 'username' not in st.session_state:
        username = None


def reset_session():
    st.session_state.logged = False
    st.session_state.username = ""
