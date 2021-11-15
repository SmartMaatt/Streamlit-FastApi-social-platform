import streamlit as st
from datetime import datetime


def home(db, user):
    current_user = db.child('Users').child(user['localId']).child('Data').get(user['idToken']).val()
    col1, col2 = st.columns(2)

    with col1:
        try:
            profile_image = current_user['Image']
            st.image(profile_image, use_column_width=True)
        except KeyError:
            st.info("No profile picture! Go to Edit Profile and choose one.")

        post = st.text_input("Let's share my current mood as a post!", max_chars=100)
        add_post = st.button('Share Post')

    if add_post:
        if len(post) > 0:
            st.balloons()
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            post = {'Post:': post, 'Timestamp': dt_string}
            db.child('Users').child(user['localId']).child("Data/Posts").push(post, user['idToken'])
            st.experimental_rerun()
        else:
            st.warning('Your post is empty!')

    # col for Post Display
    with col2:
        try:
            all_posts = current_user['Posts']
            for post in all_posts.values():
                st.code(post, language='')
        except KeyError:
            st.info("You don't have any posts!")
