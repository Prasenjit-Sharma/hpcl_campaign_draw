import streamlit as st
import pandas as pd
from useful_methods import UsefulMethods as um
from st_pages import show_pages, add_page_title, hide_pages, Page, Section
from streamlit_extras.switch_page_button import switch_page

show_pages([Page("login.py", "Login")])

# In initial logged_in is False
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False


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
