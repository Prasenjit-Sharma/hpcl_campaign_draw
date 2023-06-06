import streamlit as st
from useful_methods import UsefulMethods as um
from st_pages import show_pages, add_page_title, hide_pages, Page, Section
from streamlit_extras.switch_page_button import switch_page


def loading():
    st.header("Bharo Aur Jeeto Dhamaka")
    st.subheader("Welcome to the Draw")
    st.session_state["data"] = df = um.reading_data()
    df = df.drop_duplicates()
    no_of_entries = len(df)
    no_of_outlets = df["Outlet"].nunique()

    st.header(f"We have {no_of_entries} participants from {no_of_outlets} outlets across 6 districts under "
                      f"Jodhpur Retail Region.")

    col1, col2 = st.columns(2)

    with col1:
        um.lottie_animation("https://assets8.lottiefiles.com/private_files/lf30_mg1iit3m.json")
        but_week = st.button("Let's Start Weekly Draw🕹️", type="primary", use_container_width=True)
        if but_week:
            show_pages([Page("pages/weekly_draw.py", "Weekly Draw")])
            switch_page("Weekly Draw")

    with col2:
        um.lottie_animation("https://assets5.lottiefiles.com/packages/lf20_touohxv0.json")
        but_mega = st.button("Let's Start Mega Draw🕹️", type="primary", use_container_width=True)
        if but_mega:
            show_pages([Page("pages/mega_draw.py", "Mega Draw")])
            switch_page("Mega Draw")


if st.session_state["is_logged_in"]:
    loading()
else:
    show_pages([Page("login.py", "Login")])