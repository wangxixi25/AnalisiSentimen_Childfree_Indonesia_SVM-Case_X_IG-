import streamlit as st
from streamlit_option_menu import option_menu
from halaman import home, dashboard, analisis_sentimen

st.set_page_config(page_title="Childfree Insight", page_icon=":bar_chart:", layout="wide")

from streamlit_option_menu import option_menu
import streamlit as st

from streamlit_option_menu import option_menu
import streamlit as st

with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Home", "Dashboard", "Analisis Sentimen"],
        icons=["house-fill", "pie-chart-fill", "chat-left-text-fill"],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {
                "padding": "5px",
                "background-color": "#f8f9fa"
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#e1eaff",
                "color": "black",
                "font-weight": "normal"
            },
            "nav-link-selected": {
                "background-color": "#4285F4",
                "color": "white",
                "font-weight": "normal"
            },
        }
    )

if selected == "Home":
    home.run()
elif selected == "Dashboard":
    dashboard.run()
elif selected == "Analisis Sentimen":
    analisis_sentimen.run()
