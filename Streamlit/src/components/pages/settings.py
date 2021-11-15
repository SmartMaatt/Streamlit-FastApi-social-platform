import io
import os
import streamlit as st
from PIL import Image
from requests.exceptions import ConnectionError

from ..backend_connection import post_image_to_backend

profile_file_name = 'tmp.png'
backend_url = "http://fastapi:8000/image-edit/crop-profile-image"

def settings(db, storage, user):
    try:
        image = db.child('Users').child(user['localId']).child('Data').get(user['idToken']).val()['Image']
        if image is not None:
            st.image(image)
            # Changing profile picture
            exp = st.expander('Change profile image')
            with exp:
                input_image = st.file_uploader("Insert image", type=['jpg', 'png'], accept_multiple_files=False)
                upload_new = st.button('Upload')
                if upload_new:
                    if input_image:
                        setup_profile_image(input_image, profile_file_name, user['localId'], db, user, storage)
                    else:
                        st.warning("Didn't set a new profile picture file!")
    except KeyError:
        st.info("No profile picture yet")
        input_image = st.file_uploader("Insert image", type=['jpg', 'png'], accept_multiple_files=False)
        upload_new = st.button('Upload')
        if upload_new:
            if input_image:
                setup_profile_image(input_image, profile_file_name, user['localId'], db, user, storage)
            else:
                st.warning("Didn't set a profile picture file!")


def setup_profile_image(input_image, image_path: str, uid, db, user, storage):
    try:
        cropped_image = crop_profile_image(input_image)
        st.success('Your profile picture has been changed successfully!')
        st.subheader("Your new profile picture:")
        st.image(cropped_image)
        upload_profile_image(image_path, uid, db, user, storage)
        st.experimental_rerun()
    except ConnectionError:
        st.error("Server connection error!")
        st.error("Sorry but picture can't be processed right now. Try again later.")


def crop_profile_image(input_image):
    converted_image = post_image_to_backend(input_image, backend_url)
    converted_image = Image.open(io.BytesIO(converted_image.content)).convert("RGB")
    converted_image.save(profile_file_name, "PNG")
    return converted_image


def upload_profile_image(image_path: str, uid, db, user, storage):
    firebase_upload = storage.child(uid).put(image_path, user['idToken'])
    imgdata_url = storage.child(uid).get_url(firebase_upload['downloadTokens'])
    os.remove(profile_file_name)

    db.child('Users').child(user['localId']).child("Data/Image").set(imgdata_url, user['idToken'])
