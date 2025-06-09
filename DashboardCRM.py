import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_option_menu import option_menu
import webbrowser as webbrowser
import time, webbrowser, pyautogui
from datetime import datetime
import pywhatkit
import pandas as pd
import matplotlib.pyplot as plt

def Dashboard():
    st.markdown("DASHBOARDDD")

    conn = st.connection("gsheets", type=GSheetsConnection)

    existing_data = conn.read(worksheet="SEGUIMIENTO",usecols=list(range(7)),ttl=7)
    mensaje_data = conn.read(worksheet="MENSAJES",usecols=list(range(3)),ttl=3)

    clientes_antiguos = conn.read(worksheet="MENSAJE_DIARIO",usecols=list(range(6)),ttl=6)

    fig, ax = plt.subplots()
    ax.bar([1, 2, 3], [3, 2, 1])
    st.pyplot(fig)
