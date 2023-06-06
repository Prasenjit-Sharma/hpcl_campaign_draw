import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
# Disable certificate verification (Not necessary always)
import ssl
import requests
from streamlit_lottie import st_lottie, st_lottie_spinner
import io


class UsefulMethods:

    @staticmethod
    @st.cache_data(show_spinner=False)
    def read_gsheet():
        ssl._create_default_https_context = ssl._create_unverified_context
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope)

        sheet_url = st.secrets["gsheets"]["private_gsheets_url"]
        sheet_name = st.secrets["gsheets"]["sheet_name"]

        # Create a connection to the Google Sheet
        client2 = gspread.authorize(credentials=credentials)
        # Read Data from gsheet
        sheet = client2.open_by_url(sheet_url).worksheet(sheet_name)
        df = pd.DataFrame(sheet.get_all_records())
        return df

    @staticmethod
    def load_lottie_url(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    @staticmethod
    def reading_data():
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_bPtkGeNd9y.json"
        lottie_json = UsefulMethods.load_lottie_url(url=lottie_url)
        with st_lottie_spinner(lottie_json, key="download", width=400):
            df = UsefulMethods.read_gsheet()
            df = UsefulMethods.clean_data(df)
            return df

    @staticmethod
    def clean_data(df):
        def area(row):
            if row['District'] == 'JALORE' or row['District'] == 'BARMER':
                return 'BARMER'
            elif row['District'] == 'JAISALMER' or row['District'] == 'BIKANER':
                return 'BIKANER'
            else:
                return row['District']
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df['Sales Area'] = df.apply(area, axis=1)
        # Sales Area

        return df

    @staticmethod
    def lottie_animation(url):
        lottie_url = url
        lottie_json = UsefulMethods.load_lottie_url(url=lottie_url)
        st_lottie(lottie_json, width=200, height=200)

    @staticmethod
    def weekly_draw(start, end, min_ent):
        gifts = ["Head Set", "Bed Sheet", "Bag Pack", "Tiffin Box"]
        winners = pd.DataFrame()
        df = st.session_state["data"]
        df = df[df['Date'].between(start, end)]  # In between dates
        dealers = df['Outlet'].unique()
        for dealer in dealers:
            count = df['Outlet'].value_counts()[dealer]
            if count > min_ent:
                fil_df = df[df['Outlet'] == dealer]
                for gift in gifts:
                    winner = fil_df.sample()
                    winner['Gift'] = gift
                    winner['Outlet'] = dealer
                    winners = pd.concat([winners,winner],axis=0)
        return winners

    @staticmethod
    def mega_draw(start,end):
        gifts = ["Air Cooler", "Washing Machine", "Mobile Phone", "Bluetooth Speaker","Mixer Juicer"]
        winners = pd.DataFrame()
        df = st.session_state["data"]
        df = df[df['Date'].between(start, end)]  # In between dates
        sales_areas = df['Sales Area'].unique()
        for sales_area in sales_areas:
            fil_df = df[df['Sales Area'] == sales_area]
            for gift in gifts:
                winner = fil_df.sample()
                winner['Gift'] = gift
                winner['Sales Area'] = sales_area
                winners = pd.concat([winners, winner], axis=0)
        return winners



    @staticmethod
    def excel_write(df):
        # buffer to use for excel writer
        buffer = io.BytesIO()

        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.save()

            download2 = st.download_button(
                label="Download Winners as Excel",
                data=buffer,
                file_name='Winners.xlsx',
                mime='application/vnd.ms-excel',
            )
