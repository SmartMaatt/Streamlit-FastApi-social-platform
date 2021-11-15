import requests.exceptions
import streamlit as st


def login(email, password, db, auth, reset_session):
    login_button = st.sidebar.button("Login")

    if login_button or st.session_state.logged:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged = True
            st.session_state.username = db.child('Users').child(user['localId']).child('Data/Handle').get(user['idToken']).val()
            return user
        except (TypeError, requests.exceptions.HTTPError):
            st.error(f'Incorrect user or password!')
            reset_session()
