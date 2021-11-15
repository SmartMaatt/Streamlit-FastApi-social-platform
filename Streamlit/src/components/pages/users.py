import streamlit as st


def users(db, user):
    handles = [user.val()['Data']["Handle"] for user in db.child('Users').get(user['idToken'])]
    handles_len = len(handles)
    st.write('Total users here: ' + str(handles_len))

    friend_choice = st.selectbox('Chose user', handles)
    show_profile = st.button('Show Profile')

    if show_profile:
        st.subheader(friend_choice)
        col1, col2 = st.columns(2)
        user_by_handle = db.child('Users').order_by_child("Data/Handle").equal_to(friend_choice).get(user['idToken'])[0].val()
        user_data = user_by_handle['Data']

        with col1:
            # Show the chosen Profile
            try:
                profile_image = user_data['Image']
                st.image(profile_image, use_column_width=True)
            except KeyError:
                st.info(f"User {friend_choice} doesn't have profile picture yet!")

        with col2:
            # All posts
            try:
                all_posts = user_data['Posts']
                for post in all_posts.values():
                    st.code(post, language='')
            except KeyError:
                st.info(f"User {friend_choice} doesn't have posts yet!")
