import pandas as pd
import numpy as np
import streamlit as st

from utils.import_data_functions import * 
from utils.create_session_id import *
from utils.filter_transaction import *

session_id = get_session_id()


def calculate_all_the_user_data(transaction_data, session_id):
    '''
    Calculate user metrics by user:
    - number of transactions last 30 days
    - number of transactions last 90 days
    - number of transactions last 365 days
    - number of transactions total
    - last 30 days purchased total
    - last 90 days purchased total
    - last 365 days purchased total
    - avarage order value
    - total purchased value
    - days since first purchase
    - days since last purchase
    - days between orders
    '''
    sidebar = st.sidebar
    empty_space = sidebar.empty()
    with sidebar:
        with empty_space:
            st.markdown("Calculating user metrics...")

    td_raw = transaction_data.copy()

    # Ensure transaction_date is in datetime format
    td_raw['transaction_date'] = pd.to_datetime(td_raw['transaction_date'])

    td_summary = td_raw.groupby(['user_id']).agg(
        last_30_days_transactions=('invoice_id', lambda x: x[td_raw.loc[x.index, 'transaction_date'] >= pd.Timestamp.today() - pd.DateOffset(days=30)].nunique()),
        last_90_days_transactions=('invoice_id', lambda x: x[td_raw.loc[x.index, 'transaction_date'] >= pd.Timestamp.today() - pd.DateOffset(days=90)].nunique()),
        last_365_days_transactions=('invoice_id', lambda x: x[td_raw.loc[x.index, 'transaction_date'] >= pd.Timestamp.today() - pd.DateOffset(days=365)].nunique()),
        total_transactions=('invoice_id', 'nunique'),
        last_30_days_purchased_total=('sales_value', lambda x: x[td_raw.loc[x.index, 'transaction_date'] >= pd.Timestamp.today() - pd.DateOffset(days=30)].sum()),
        last_90_days_purchased_total=('sales_value', lambda x: x[td_raw.loc[x.index, 'transaction_date'] >= pd.Timestamp.today() - pd.DateOffset(days=90)].sum()),
        last_365_days_purchased_total=('sales_value', lambda x: x[td_raw.loc[x.index, 'transaction_date'] >= pd.Timestamp.today() - pd.DateOffset(days=365)].sum()),
        average_order_value=('sales_value', lambda x: x.sum() / td_raw.loc[x.index, 'invoice_id'].nunique()),
        total_purchased_value=('sales_value', 'sum'),
        days_since_first_purchase=('transaction_date', lambda x: (pd.Timestamp.today() - x.min()).days),
        days_since_last_purchase=('transaction_date', lambda x: (pd.Timestamp.today() - x.max()).days),
        # this is not working because of the following error: AttributeError: 'DatetimeArray' object has no attribute 'diff'
        days_between_orders=('transaction_date', lambda x: pd.Series(x.sort_values().unique()).diff().dropna().mean().days)
        #days_between_orders=('transaction_date', lambda x: x.sort_values().unique().diff().mean().days)
    ).reset_index()

    with sidebar:
        with empty_space:
            st.markdown(" ")

    return td_summary

def filter_user_data(transaction_data, selected_user_id):
    t_data = transaction_data.copy()
    t_data_user = t_data[t_data['user_id'] == selected_user_id]

    # order by transaction_date
    t_data_user = t_data_user.sort_values(['transaction_date'])

    return t_data_user

def filter_user_data_for_selected_user(transacttion_data_summary, selected_user_id):
    return transacttion_data_summary[transacttion_data_summary['user_id'] == selected_user_id]

def single_user_statistics_apply_filters_and_recalculate(session_id, data, segment_filter, start_date, end_date):
    # filter the data
    st.session_state.transaction_maped_dataset_filtered = filter_transaction_data(session_id, data,
                                                                                  segment_filter,
                                                                                  start_date,
                                                                                  end_date
                                                                                 )
    st.session_state.total_users_summary_data_filtered = calculate_all_the_user_data(st.session_state.transaction_maped_dataset_filtered , get_session_id())
    st.session_state.unique_user_id_list = st.session_state.transaction_maped_dataset_filtered['user_id'].unique()