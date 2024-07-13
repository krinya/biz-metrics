import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu

from utils.pages_and_titles import *
from utils.read_config import *
from utils.create_filter_defaul_values import *
from utils.import_data_functions import *
from utils.create_session_id import *

session_id = get_session_id()


def filter_transaction_data(session_id, data, segment_filter, date_min_filter, date_max_filter):

    filtered_data = data.copy()

    # if 'All' is in the segment filter list, do nothing
    if 'All' not in segment_filter:
        filtered_data = filtered_data[filtered_data['segment'].isin(segment_filter)]
    if 'All' in segment_filter:
        filtered_data = filtered_data

    filtered_data = filtered_data[(filtered_data['transaction_date'] >= date_min_filter) & (filtered_data['transaction_date'] <= date_max_filter)]
    
    st.session_state.transaction_maped_dataset_filtered = filtered_data

    return st.session_state.transaction_maped_dataset_filtered