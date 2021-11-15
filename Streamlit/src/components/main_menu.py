import streamlit as st


def main_menu(cards_to_select, reset_session):
    col1, col2 = st.columns(2)
    with col1:
        selected_card = st.radio(f"Hello {st.session_state.username}", cards_to_select)
    with col2:
        if st.button("Log Out"):
            reset_session()
            st.experimental_rerun()

    return selected_card
