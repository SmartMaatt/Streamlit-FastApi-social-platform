from ..classes.dataframe import Dataframe
import pandas as pd
import streamlit as st
import json
import random
import string


def dataframes(db, user):
    user_dataframes = db.child('Users').child(user['localId']).child('Belongings/Dataframes').get(user['idToken']).val()
    try:
        owned_dataframes = generate_dataframe_packet(user_dataframes['Owned'], db, user)
    except (TypeError, KeyError):
        owned_dataframes = []

    try:
        collaborated_dataframes = generate_dataframe_packet(user_dataframes['Collaborations'], db, user)
    except (TypeError, KeyError):
        collaborated_dataframes = []

    exp = st.expander('Upload new dataframe')
    with exp:
        with st.form("upload-dataframe-form", clear_on_submit=True):
            dataframe_name = st.text_input(label="Name of your dataset", max_chars=50)
            dataframe_file = st.file_uploader(label="Upload your CSV or Excel file", type=['csv', 'xlsx'],
                                              accept_multiple_files=False)
            submit = st.form_submit_button("Upload")

        if submit:
            if len(dataframe_name) > 0:
                if dataframe_file is not None:
                    try:
                        df = pd.read_csv(dataframe_file)
                    except UnicodeDecodeError:
                        df = pd.read_excel(dataframe_file)

                    df_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(28))
                    dataframe_push = {
                        'Belongings': {
                            'Collaborators': False,
                            'Owner': user['localId']
                        },
                        'Data': {
                            'Title': dataframe_name,
                            'ID': df_id,
                            'Content': json.loads(df.to_json(orient='split'))
                        }
                    }

                    st.success("Your dataframe has been added successfully!")
                    db.child('Users').child(user['localId']).child('Belongings/Dataframes/Owned').child(df_id).set(True, user['idToken'])

                    db.child('Dataframes').child(df_id).update(dataframe_push, user['idToken'])
                    st.experimental_rerun()
                else:
                    st.error("Dataframe file input is empty!")
            else:
                st.error("Name of dataframe is empty!")

    st.subheader("Owned dataframes")
    if owned_dataframes:
        for df in owned_dataframes:
            df.draw_dataset_as_owner()
    else:
        st.info("No dataframes to display!")

    st.subheader("Collaborated dataframes")
    if collaborated_dataframes:
        for df in collaborated_dataframes:
            df.draw_dataset_as_collaborator()
    else:
        st.info("No dataframes to display!")


def generate_dataframe_packet(dataframe_ids, db, user):
    try:
        return [
            Dataframe(
                df['Data']['ID'],
                df['Data']['Title'],
                df['Belongings']['Owner'],
                df['Belongings']['Collaborators'],
                df['Data']['Content'],
                db, user
            )
            for df in [db.child('Dataframes').child(df_id).get(user['idToken']).val() for df_id in dataframe_ids]
        ]
    except (AttributeError, TypeError):
        return []
