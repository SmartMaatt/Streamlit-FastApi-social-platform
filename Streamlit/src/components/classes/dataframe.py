import requests
import streamlit as st
import pandas as pd


class Dataframe:
    def __init__(self, df_id: str, title: str, owner_id: str, collaborators, content, db, user):
        self.df_id = df_id
        self.title = title
        self.owner_id = owner_id
        self.collaborators = collaborators
        self.content = content

        self.db = db
        self.user = user
        self.owner_name = self.get_owner_handle(owner_id)

    def draw_dataset_as_owner(self):
        exp = st.expander(self.title)
        with exp:
            st.dataframe(pd.DataFrame(self.content['data'], columns=self.content['columns']))
            self.display_dataframe_info()

            collaborator_to_remove = self.display_collaborators_list(label="Remove collaborator", btn="Remove")
            if collaborator_to_remove:
                if self.remove_collaborator_by_name(collaborator_to_remove):
                    st.success(
                        "User " + collaborator_to_remove + " has been successfully removed from collaborators list!")
                else:
                    st.error("Upsss, something went wrong! Try again later.")
                st.experimental_rerun()

            collaborator_to_add = self.display_users_list(label="Add new collaborator", btn="Add")
            if collaborator_to_add:
                if self.add_collaborator(collaborator_to_add):
                    st.success("User " + collaborator_to_add + " has been successfully added to collaborators list!")
                else:
                    st.error("Upsss, something went wrong! Try again later.")
                st.experimental_rerun()

            dataframe_to_remove = st.button('Remove dataframe', key=self.df_id)
            if dataframe_to_remove:
                if self.remove_dataframe():
                    st.success("Dataframe " + self.title + " has been removed successfully!")
                else:
                    st.error("Upsss, something went wrong! Try again later.")
                st.experimental_rerun()

    def draw_dataset_as_collaborator(self):
        exp = st.expander(self.title)
        with exp:
            st.dataframe(pd.DataFrame(self.content['data'], columns=self.content['columns']))
            self.display_dataframe_info()

            leave_dataframe = st.button('Leave dataframe', key=self.df_id)
            if leave_dataframe:
                if self.remove_collaborator_by_id(self.user['localId']):
                    st.success("You have successfully left dataframe!")
                else:
                    st.error("Upsss, something went wrong! Try again later.")
                st.experimental_rerun()

    def display_dataframe_info(self):
        if self.collaborators:
            collaborators = ''.join(
                [self.db.child('Users').child(collaborator_id).child('Data/Handle').get(
                    self.user['idToken']).val() + ", "
                 for collaborator_id in self.collaborators.keys()
                 ])
            collaborators = collaborators[:-1]
        else:
            collaborators = "None"

        st.markdown(
            "**Name: **" + self.title + " | " + "**Owner: **" + self.owner_name + " | " + "**Collaborators: **" + collaborators)

    def display_collaborators_list(self, label: str, btn: str):
        if self.collaborators is not False:
            with st.form("collaborators-" + self.df_id, clear_on_submit=True):
                handles = [self.db.child('Users').order_by_child('Data/ID').equal_to(col_id).get(
                    self.user['idToken'])[0].val()['Data']['Handle']
                           for col_id in self.collaborators.keys()
                           ]

                selected_user = st.selectbox(label, handles)
                submit = st.form_submit_button(btn)

            if submit:
                return selected_user
        return None

    def display_users_list(self, label: str, btn: str):
        with st.form("display-users-" + self.df_id, clear_on_submit=True):
            query = self.db.child('Users').get(self.user['idToken'])

            if self.collaborators is not False:
                handles = [user.val()["Data"]["Handle"] for user in query if
                           (user.val()["Data"]["ID"] not in self.collaborators.keys())]
            else:
                handles = [user.val()["Data"]["Handle"] for user in query]

            handles.remove(self.owner_name)
            selected_user = st.selectbox(label, handles)
            submit = st.form_submit_button(btn)

        if submit:
            return selected_user

    def add_collaborator(self, user_name: str):
        try:
            user_by_handle = self.db.child('Users').order_by_child("Data/Handle").equal_to(user_name).get(self.user['idToken'])[0].val()
            user_id = user_by_handle['Data']['ID']

            if not self.collaborators:
                self.collaborators = {user_id: True}
            else:
                self.collaborators.update({user_id: True})

            self.db.child('Dataframes').child(self.df_id).child('Belongings').update({'Collaborators': self.collaborators}, self.user['idToken'])
            self.db.child('Users').child(user_id).child('Belongings/Dataframes/Collaborations').child(self.df_id).set(True, self.user['idToken'])
            return True
        except requests.exceptions.HTTPError as err:
            st.error(err)
            return False

    def remove_collaborator_by_name(self, user_name):
        try:
            user_id = self.db.child('Users').order_by_child("Data/Handle").equal_to(user_name).get(
                self.user['idToken'])[0].val()['Data']['ID']

            if len(self.collaborators) > 1:
                self.collaborators.pop(user_id)
            else:
                self.collaborators = False

            self.db.child('Dataframes').child(self.df_id).child('Belongings').update(
                {'Collaborators': self.collaborators}, self.user['idToken'])
            self.db.child('Users').child(user_id).child('Belongings/Dataframes/Collaborations').child(
                self.df_id).remove(self.user['idToken'])
            return True
        except (requests.exceptions.HTTPError, IndexError):
            return False

    def remove_collaborator_by_id(self, user_id):
        try:
            if len(self.collaborators) > 1:
                self.collaborators.pop(user_id)
            else:
                self.collaborators = False

            self.db.child('Dataframes').child(self.df_id).child('Belongings').update(
                {'Collaborators': self.collaborators}, self.user['idToken'])
            self.db.child('Users').child(user_id).child('Belongings/Dataframes/Collaborations').child(
                self.df_id).remove(self.user['idToken'])
            return True
        except (requests.exceptions.HTTPError, IndexError) as err:
            st.error(err)
            return False

    def remove_dataframe(self):
        try:
            if self.collaborators:
                for collaborator in self.collaborators.keys():
                    self.db.child('Users').child(collaborator).child('Belongings/Dataframes/Collaborations').child(self.df_id).remove(self.user['idToken'])

            self.db.child('Dataframes').child(self.df_id).remove(self.user['idToken'])
            self.db.child('Users').child(self.owner_id).child('Belongings/Dataframes/Owned').child(self.df_id).remove(self.user['idToken'])
            return True
        except requests.exceptions.HTTPError:
            return False

    def get_owner_handle(self, user_id: str):
        try:
            return self.db.child('Users').child(user_id).child('Data/Handle').get(self.user['idToken']).val()
        except requests.exceptions.HTTPError:
            return 'Unknown'
