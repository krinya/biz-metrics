import pandas as pd
import streamlit as st
import numpy as np

from utils.create_session_id import get_session_id

@st.cache_resource(show_spinner="Getting the default values for the filters...")
def get_segment_default_values(dataset, session_id):
    
    segment_default_values = dataset['segment'].unique()
    # add 'All' to the beginning of the list
    segment_default_values = np.insert(segment_default_values, 0, 'All')
    st.session_state.segment_default_values = segment_default_values
    
    return segment_default_values