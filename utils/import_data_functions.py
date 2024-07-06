import pandas as pd
import numpy as np
import streamlit as st

def check_if_date_is_loaded():
    if 'transaction_maped_dataset' not in st.session_state:
        st.error("Please select, import data and map the columns first on the import page.")
        st.stop()