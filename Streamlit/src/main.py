import pyrebase
import streamlit as st

from assets.builder import Builder
from components import session_config

from config import firebaseConfig
from components.sign_up import sign_up
from components.login import login
from components.main_menu import main_menu

from components.pages.home import home
from components.pages.settings import settings
from components.pages.users import users
from components.pages.dataframes import dataframes

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

# Custom component builder
components_builder = Builder('assets/styles/', ['main.css'], 'assets/scripts/', ['main.js'])
st.markdown(components_builder.generate_style_component, unsafe_allow_html=True)

session_config.initialize_session()

if not st.session_state.logged:
    # Authentication
    st.sidebar.title("Streamlit test app")
    choice = st.sidebar.selectbox('Choose action', ['Login', 'Sign up'])
    email = st.sidebar.text_input('Email address')
    password = st.sidebar.text_input('Password', type='password')

    # Sign up to app
    if choice == 'Sign up':
        sign_up(email, password, db, auth, session_config.reset_session)

    # Login to app
    if choice == 'Login':
        login(email, password, db, auth, session_config.reset_session)

else:
    selected_card = main_menu(['Home', 'Users', 'Dataframes', 'Settings'], session_config.reset_session)

    if st.session_state.logged:
        if selected_card == 'Home':
            home(db, st.session_state.user)
        elif selected_card == 'Users':
            users(db, st.session_state.user)
        elif selected_card == 'Dataframes':
            dataframes(db, st.session_state.user)
        elif selected_card == 'Settings':
            settings(db, storage, st.session_state.user)
    else:
        st.info(f"User logged off successfully")
