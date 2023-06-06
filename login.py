import streamlit as st
import pandas as pd
from useful_methods import UsefulMethods as um
from st_pages import show_pages, add_page_title, hide_pages, Page, Section
from streamlit_extras.switch_page_button import switch_page

# In initial logged_in is False
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state.page = -1

# Empty Placeholder to store opening image and replace with the Data Choice Dashboard after Log in
placeholder = st.empty()
df = pd.DataFrame()

# Login Screen
if not st.session_state["is_logged_in"]:
    with placeholder.container():
        col1, inter_col_space, col2 = st.columns([2, 1, 2])

        st.image(
            "https://i1.wp.com/hrnxt.com/wp-content/uploads/2021/07/Hindustan-Petroleum.jpg?resize=580%2C239&ssl=1",
            use_column_width=True
            # Manually Adjust the width of the image as per requirement
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        but_login = st.button(label="Let the Games Begin🕹️", type="primary")

        if but_login:
            if (username in st.secrets["passwords"] and password == st.secrets["passwords"][username]):
                st.session_state["is_logged_in"] = True
                show_pages([Page("pages/loading_data.py", "Load Data")])
                switch_page("load data")
                placeholder = st.empty()
            else:
                st.error("😕 User not known or password incorrect")
else:
    show_pages([Page("login.py", "Login")])
# When Logged In
# if st.session_state.page == 0:
#     placeholder = st.empty()
#     with placeholder.container():
#         st.header("Bharo Aur Jeeto Dhamaka")
#         st.subheader("Welcome to the Draw")
#         but_load = st.button("Let the Games Begin🕹️", type="primary", use_container_width=True)
#
#         if but_load:
#             df = um.reading_data()
#             st.session_state.page = 1
#
# # Start of Draw
# elif st.session_state.page == 1:
#
#
#     df = df.drop_duplicates()
#     no_of_entries = len(df)
#     no_of_outlets = df["Outlet"].nunique()
#     # st.dataframe(df.head(), use_container_width=True)
#     with placeholder.container():
#         st.header(f"We have {no_of_entries} participants from {no_of_outlets} outlets across 6 districts under "
#                   f"Jodhpur Retail Region.")
#         um.lottie_animation()
#         but_draw = st.button("Let's Start The Lucky Draw🕹️", type="primary", use_container_width=True)
#
#     if but_draw:
#
#         st.session_state.page = 2
#
#
# elif st.session_state.page == 2:
#     with placeholder.container():
#         st.header("Its Time to Find the Winner")
#         tab1, tab2 = st.tabs(["Week 1","Week 2"])
#
#         with tab1:
#             st.write("Welcome to Week 1 Draw")