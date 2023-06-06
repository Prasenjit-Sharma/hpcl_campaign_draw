import streamlit as st
from useful_methods import UsefulMethods as um
from st_pages import show_pages, add_page_title, hide_pages, Page, Section
from streamlit_extras.switch_page_button import switch_page


def weekly():
    but_home = st.button("Home", type="primary", use_container_width=True)
    if but_home:
        show_pages([Page("pages/loading_data.py", "Home")])
        switch_page("Home")
    st.header("Weekly Draw")
    placeholder =st.empty()
    with placeholder.container():
        col1,col2,col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start Date")
            um.lottie_animation("https://assets8.lottiefiles.com/private_files/lf30_mg1iit3m.json")
        with col2:
            end_date = st.date_input("End Date")

        with col3:
            min_ent = st.number_input("Minimum No. of Entries", min_value=30)
            um.lottie_animation("https://assets5.lottiefiles.com/packages/lf20_touohxv0.json")
        draw = st.button("Draw", type="primary", use_container_width=True)
    if draw:
        df = um.weekly_draw(start_date,end_date,min_ent)
        with placeholder.container():
            st.dataframe(df)
            um.excel_write(df)


if st.session_state["is_logged_in"]:
    weekly()
else:
    show_pages([Page("login.py", "Login")])