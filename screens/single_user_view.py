import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.pages_and_titles import *
from utils.read_config import *
from utils.import_data_functions import *
from utils.create_session_id import *

# read the config file
config_all = read_config()
general = read_config(section = 'general')
sus_cf = read_config(section = 'single_user_view')

st.title("Single User View")
st.markdown("Here you can see some statistics about one users.")

st.session_state.transaction_maped_dataset = check_if_data_is_loaded(get_session_id())

@st.cache_resource(show_spinner="Calculating user metics. Please wait...")
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
        days_between_orders=('transaction_date', lambda x: x.sort_values().diff().mean().days)
    ).reset_index()

    return td_summary


st.session_state.total_users_summary_data_raw = calculate_all_the_user_data(st.session_state.transaction_maped_dataset, get_session_id())

if sus_cf['developer_mode']:
    st.markdown("## transaction_maped_dataset - Raw Data")
    st.dataframe(st.session_state.transaction_maped_dataset, use_container_width=True, hide_index=True)
    st.markdown("## total_users_summary_data - Raw Data")
    st.dataframe(st.session_state.total_users_summary_data_raw, use_container_width=True, hide_index=True)

# st.markdown("## User Selection")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
col1, col2 = st.columns([1, 1])
with col1:
    unique_user_id_list = st.session_state.transaction_maped_dataset['user_id'].unique()
    st.selectbox("Select a user", unique_user_id_list, key="selected_user_id")
with col2:
    st.checkbox("Show selected user data", key="show_selected_user_data", value=False)

# filter the user data for the selected user
@st.cache_data
def filter_user_data(transaction_data, selected_user_id):
    t_data = transaction_data.copy()
    t_data_user = t_data[t_data['user_id'] == selected_user_id]

    # order by transaction_date
    t_data_user = t_data_user.sort_values(['transaction_date'])

    return t_data_user

@st.cache_data
def filter_user_data_for_selected_user(transacttion_data_summary, selected_user_id):
    return transacttion_data_summary[transacttion_data_summary['user_id'] == selected_user_id]

st.session_state.selected_user_data = filter_user_data(st.session_state.transaction_maped_dataset, st.session_state.selected_user_id)
st.session_state.selected_user_data_summary = filter_user_data_for_selected_user(st.session_state.total_users_summary_data_raw, st.session_state.selected_user_id)


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

