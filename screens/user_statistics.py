import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.pages_and_titles import *
from utils.read_config import *
from utils.import_data_functions import *

# read the config file
config_all = read_config()
general = read_config(section = 'general')
us_cf = read_config(section = 'user_statistics')

st.title("User Statistics")
st.markdown("Here you can see some statistics about the users.")

check_if_date_is_loaded()

if us_cf['developer_mode']:
    st.markdown("## transaction_maped_dataset - Raw Data")
    st.dataframe(st.session_state.transaction_maped_dataset, use_container_width=True, hide_index=True)


def cummulative_users_calculation(data, aggregation_level = 'day', lookback = 30):

    min_date = data['transaction_date'].min()
    max_date = data['transaction_date'].max()
    diff_max_min_date_in_days = (max_date - min_date).days
    st.write(f"Data is between {min_date} and {max_date}.")
    st.write(f"Data is {diff_max_min_date_in_days} days long.")

    # create a date range with all the days between the min and max date
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    date_range_df = pd.DataFrame(date_range, columns=['date'])

    progress_bar_cummulative_users = st.progress(0, text='Calculating cummulative users... Please wait.')

    # create a dataframe with the total unique users until that day who we interacted with
    cummulative_users_df = pd.DataFrame()
    i = 0
    for date in date_range:
        pb_value = i / diff_max_min_date_in_days
        progress_bar_cummulative_users.progress(pb_value)

        date = pd.Timestamp(date)
        date_minus_lookback = date - pd.DateOffset(days=lookback)

        data_filtered_cummulative = data[data['transaction_date_time'] <= date]
        unique_users_to_date = data_filtered_cummulative['user_id'].nunique()

        data_filtered_lookback = data_filtered_cummulative[data_filtered_cummulative['transaction_date_time'] >= date_minus_lookback]
        unique_users_lookback = data_filtered_lookback['user_id'].nunique()

        cummulative_users_until_date = pd.DataFrame({'date': [date],
                                                     'day': [i + 1],
                                                     'users_to_date': [unique_users_to_date],
                                                     'users_lookback': [unique_users_lookback]})
        
        cummulative_users_df = pd.concat([cummulative_users_df, cummulative_users_until_date], ignore_index=True)

        i += 1

    # convert date to date
    cummulative_users_df['date'] = pd.to_datetime(cummulative_users_df['date']).dt.date

    return cummulative_users_df

st.markdown("### Options")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    # lookback period in days number input
    lookback_days_default = int(us_cf['lookback_days_default'])
    lookback_period = st.number_input("Lookback period in days", min_value=1, value=lookback_days_default, key='lookback_period_option')

if 'cummulative_users' not in st.session_state:
    st.session_state.cummulative_users = cummulative_users_calculation(st.session_state.transaction_maped_dataset, lookback = st.session_state.lookback_period_option)

# create a button that recalculates the cummulative users if pressed
if st.button("Recalculate cummulative users"):
    st.session_state.cummulative_users = cummulative_users_calculation(st.session_state.transaction_maped_dataset, lookback = st.session_state.lookback_period_option)

st.markdown("## Cummulative Users")
st.dataframe(st.session_state.cummulative_users, use_container_width=True, hide_index=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("## Cummulative Users - Users to Date")
    fig = px.line(st.session_state.cummulative_users, x='date', y='users_to_date')
    st.plotly_chart(fig, use_container_width=True, theme=None)

with col2:
    st.markdown(f"## Cummulative Users - Using {st.session_state.lookback_period_option} days")
    fig2 = px.line(st.session_state.cummulative_users, x='date', y='users_lookback')
    st.plotly_chart(fig2, use_container_width=True, theme=None)