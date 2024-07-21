import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.pages_and_titles import *
from utils.read_config import *
from utils.import_data_functions import *
from utils.create_session_id import *
from utils.create_filter_defaul_values import *
from utils.filter_transaction import *
from utils.user_view_functions import *


# read the config file
config_all = read_config()
general = read_config(section = 'general')
sus_cf = read_config(section = 'single_user_view')

st.title("Single User View")
st.markdown("Here you can see some statistics about one users.")

st.session_state.transaction_maped_dataset = check_if_data_is_loaded(get_session_id())

st.markdown("### Filters")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    # filter for segment
    # create a list of unique values
    st.session_state.segment_list_all = get_segment_default_values(st.session_state.transaction_maped_dataset, get_session_id())
    # create a multi-select dropdown
    st.multiselect('Select Segment', st.session_state.segment_list_all, default=['All'], key='segment_filter_transactions')
with col2:
    st.date_input('Select Start Date', key='start_date_filter_transactions', value=st.session_state.transaction_maped_dataset['transaction_date'].min())
with col3:
    st.date_input('Select End Date', key='end_date_filter_transactions', value='today')

# create a button that filteres the data
st.button('Apply filters / Recalculate Data', key='filter_data_button', on_click=single_user_statistics_apply_filters_and_recalculate,
          args=(session_id, st.session_state.transaction_maped_dataset,
                st.session_state.segment_filter_transactions,
                st.session_state.start_date_filter_transactions,
                st.session_state.end_date_filter_transactions))

if 'transaction_maped_dataset_filtered' not in st.session_state:
    st.session_state.transaction_maped_dataset_filtered = filter_transaction_data(get_session_id(), st.session_state.transaction_maped_dataset,
                                                                                  st.session_state.segment_filter_transactions,
                                                                                  st.session_state.start_date_filter_transactions,
                                                                                  st.session_state.end_date_filter_transactions
                                                                                 )
if 'total_users_summary_data_filtered' not in st.session_state:
    st.session_state.total_users_summary_data_filtered = calculate_all_the_user_data(st.session_state.transaction_maped_dataset_filtered , get_session_id())
    st.session_state.unique_user_id_list = st.session_state.transaction_maped_dataset['user_id'].unique()

if 'unique_user_id_list' not in st.session_state:
    st.session_state.unique_user_id_list = st.session_state.transaction_maped_dataset['user_id'].unique()

if sus_cf['developer_mode']:
    st.markdown("## transaction_maped_dataset - Raw Data")
    st.dataframe(st.session_state.transaction_maped_dataset, use_container_width=True, hide_index=True)
    st.markdown("## transaction_maped_dataset - Filtered Data")
    st.dataframe(st.session_state.transaction_maped_dataset_filtered, use_container_width=True, hide_index=True)

# st.markdown("## User Selection")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
col1, col2 = st.columns([1, 1])
with col1:
    st.selectbox("Select a user", st.session_state.unique_user_id_list, key="selected_user_id")
with col2:
    st.checkbox("Show selected user data", key="show_selected_user_data", value=False)


st.session_state.selected_user_data = filter_user_data(st.session_state.transaction_maped_dataset_filtered, st.session_state.selected_user_id)
st.session_state.selected_user_data_summary = filter_user_data_for_selected_user(st.session_state.total_users_summary_data_filtered, st.session_state.selected_user_id)


st.markdown("## User Lifetime Values")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap='small')
emoji_to_insert = ':point_down:'
emoji_under_construction = ':construction:'
icon_working = "👇"
icon_under_construction = "🚧"
with col1:
    with st.expander(f"**Transaction count**", icon=icon_working, expanded=True):
        # st.markdown(f"### {emoji_to_insert} Transaction count")
        st.markdown(f"Total transactions:")
        st.markdown(f"{st.session_state.selected_user_data_summary['total_transactions'].values[0]}")

        st.markdown(f"Last 30 days transactions:")
        st.markdown(f"{st.session_state.selected_user_data_summary['last_30_days_transactions'].values[0]}")

        st.markdown(f"Last 90 days transactions:")
        st.markdown(f"{st.session_state.selected_user_data_summary['last_90_days_transactions'].values[0]}")

        st.markdown(f"Last 365 days transactions:")
        st.markdown(f"{st.session_state.selected_user_data_summary['last_365_days_transactions'].values[0]}")

with col2:
    with st.expander(f"**Purchase value**", icon=icon_working, expanded=True):
        #st.markdown(f"### {emoji_to_insert} Purchase value")
        st.markdown(f"Total purchased value:")
        st.markdown(f"{st.session_state.selected_user_data_summary['total_purchased_value'].values[0]:,.2f}")

        st.markdown(f"Last 30 days purchased value:")
        st.markdown(f"{st.session_state.selected_user_data_summary['last_30_days_purchased_total'].values[0]:,.2f}")

        st.markdown(f"Last 90 days purchased value:")
        st.markdown(f"{st.session_state.selected_user_data_summary['last_90_days_purchased_total'].values[0]:,.2f}")

        st.markdown(f"Last 365 days purchased value:")
        st.markdown(f"{st.session_state.selected_user_data_summary['last_365_days_purchased_total'].values[0]:,.2f}")

with col3:
    with st.expander(f"**Average order value**", icon=icon_working, expanded=True):
        #st.markdown(f"### {emoji_to_insert} Average order value")
        st.markdown(f"Average order value:")
        st.markdown(f"{st.session_state.selected_user_data_summary['average_order_value'].values[0]:,.2f}")

with col4:
    with st.expander(f"**Days**", icon=icon_working, expanded=True):
        #st.markdown(f"### {emoji_to_insert} Days")
        st.markdown(f"Days since first purchase:")
        st.markdown(f"{st.session_state.selected_user_data_summary['days_since_first_purchase'].values[0]}")

        st.markdown(f"Days since last purchase:")
        st.markdown(f"{st.session_state.selected_user_data_summary['days_since_last_purchase'].values[0]}")

        st.markdown(f"Average days between orders:")
        st.markdown(f"{st.session_state.selected_user_data_summary['days_between_orders'].values[0]:,.2f}")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    with st.expander(f"**Churn risk**", icon=icon_under_construction, expanded=True):
        # st.markdown("Under development, currently not working, just a hardcoded number.")
        st.markdown("Churn Risk:")
        churn_risk_random = np.random.randint(0, 100)
        st.markdown(f"{churn_risk_random}%")
        st.markdown("Repurchase probability:")
        repurchase_probability_random = 100 - churn_risk_random
        st.markdown(f"{repurchase_probability_random}%")
with col2:
    with st.expander(f"**Predicted Lifetime value**", icon=icon_under_construction, expanded=True):
        #st.markdown("Under development, currently not working, just a hardcoded number.")
        predicted_lifetime_value_random = np.random.randint(0, 10000)
        st.markdown("Predicted Lifetime value:")
        st.markdown(f"{predicted_lifetime_value_random}")
        predicted_365_days_value_random = np.random.randint(0, 10000)
        st.markdown("Predicted 365 days value:")
        st.markdown(f"{predicted_365_days_value_random}")
   
with col3:
    with st.expander(f"**Predicted future orders**", icon=icon_under_construction, expanded=True):
        #st.markdown("Under development, currently not working, just a hardcoded number.")
        predicted_orders_random = np.random.randint(0, 10)
        st.markdown("Predicted future orders:")
        st.markdown(f"{predicted_orders_random}")
        predicted_365_days_orders_random = np.random.randint(0, 10)
        st.markdown("Predicted 365 days orders:")
        st.markdown(f"{predicted_365_days_orders_random}")
  
with col4:
    with st.expander(f"**Inactivity Score**", icon=icon_under_construction, expanded=True):
        #st.markdown("Under development, currently not working, just a hardcoded number.")
        inactivity_score_random = np.random.randint(0, 10)
        st.markdown("Inactivity Score:")
        st.markdown(f"{inactivity_score_random}")
        empty_space = st.empty()


def create_timeline_plot(transaction_data, user_id):
    '''
    Create a timeline plot for the user from beginning to today
    '''
    td = transaction_data.copy()
    td = td[td['user_id'] == user_id]
    
    # calculate the total sales value for each invoice
    td_summary = td.groupby(['invoice_id', 'transaction_date']).agg(
        sales_value_per_invoice=('sales_value', 'sum')
    ).reset_index()

    td_summary['transaction_date'] = pd.to_datetime(td_summary['transaction_date'])
    td_summary = td_summary.sort_values('transaction_date')

    today = pd.Timestamp.today().date()

    fig_bar = px.bar(td_summary, x='transaction_date', y='sales_value_per_invoice', color='invoice_id')
    
    # set the x axis range to the first transaction date and today
    fig_bar.update_xaxes(range=[td['transaction_date'].min(), today])
    # do not show legend
    fig_bar.update_layout(showlegend=False)

    # Set the bar width to 1 day
    d = 3
    for bar in fig_bar.data:
        bar.width = d * 86400000

    return fig_bar

# st.markdown(f"### User Timeline of purchases - UserID: {st.session_state.selected_user_id}")
st.markdown("### Timeline of purchases (by invoice)")
fig_bar = create_timeline_plot(st.session_state.selected_user_data, st.session_state.selected_user_id)
st.plotly_chart(fig_bar, use_container_width=True, theme=None)
    

if st.session_state.show_selected_user_data:
    st.markdown("## Selected User Data")
    st.dataframe(st.session_state.selected_user_data, use_container_width=True, hide_index=True)
    st.markdown("## Selected User Data Summary")
    st.dataframe(st.session_state.selected_user_data_summary, use_container_width=True, hide_index=True)

