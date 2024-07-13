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


# read the config file
config_all = read_config()
general = read_config(section = 'general')
ideas_cf = read_config(section = 'ideas')
show_ideas = ideas_cf['show_ideas_default']

# if show ideas is False: st.stop()
if not show_ideas:
    st.stop()

st.title("Some other ideas")

st.markdown("## Market basket analysis")
st.markdown("Which products are bought together? To give product recommendations.")

st.markdown("## Sipmle Customer segmentation = RFM analysis")
st.markdown("Cteate Recency, Frequency, Monetary Value categories and segment customers based on these categories. Put this to the user statistics page.")

st.markdown("## Session analysis")
st.markdown("For this we need session data. Then we can analyze metrics like:")
st.markdown("Login per period, active sessions, carts created, orders processed, logins per day, payment declined")
st.markdown("Time on site, Bounce Rate, Number of pages visited, Product views, Cart adds, Time to conversion, Abandoment rate, etc.")