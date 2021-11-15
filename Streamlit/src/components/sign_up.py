import requests.exceptions
import streamlit as st


def sign_up(email, password, db, auth, reset_session):
    handle = st.sidebar.text_input('Nick name', value='Default')
    submit = st.sidebar.button('Create my account')

    if submit:
        try:
            user = auth.create_user_with_email_and_password(email, password)
            handle_check = db.child('Users').order_by_child("Data/Handle").equal_to(handle).get(user['idToken']).val()
            if len(handle_check) > 0:
                st.error(f'User with username "{handle}" already exists!')
                auth.delete_user_account(user['idToken'])
                reset_session()
            else:
                st.success('Your account has been created!')
                st.balloons()
                st.info('Login via dropdown menu')

                db.child('Users').child(user['localId']).child("Data/Handle").set(handle, user['idToken'])
                db.child('Users').child(user['localId']).child("Data/ID").set(user['localId'], user['idToken'])
                st.title('Welcome ' + handle)
        except TypeError:
            st.error(f'Invalid arguments!')
            reset_session()
        except requests.exceptions.HTTPError:
            st.error(f'User with email "{email}" already exists!')
            reset_session()
