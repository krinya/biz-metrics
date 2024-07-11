import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu

from utils.pages_and_titles import *
from utils.read_config import *
from utils.create_filter_defaul_values import *
from utils.import_data_functions import *


# read the config file
config_all = read_config()
general = read_config(section = 'general')
ts_cf = read_config(section = 'transaction_statistics')

st.title("Transaction Statistics")
st.markdown("Here you can see some statistics about transactions.")

st.session_state.transaction_maped_dataset = check_if_data_is_loaded(get_session_id())

if ts_cf['developer_mode']:
    st.markdown("## transaction_maped_dataset - Raw Data")
    st.dataframe(st.session_state.transaction_maped_dataset, use_container_width=True, hide_index=True)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    # filter for segment
    # create a list of unique values
    st.session_state.segment_list_all = get_segment_default_values(st.session_state.transaction_maped_dataset, get_session_id())
    # create a multi-select dropdown
    st.multiselect('Select Segment', st.session_state.segment_list_all, default=['All'], key='segment_filter_transactions')

# col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
sidebar = st.sidebar
with st.sidebar:
    with st.popover("Graph options", use_container_width=True):

        # select grouping for barchart
        barmode_option = ['group', 'overlay', 'relative']
        barmode_default = ts_cf['graph_options']['barmode_default']
        st.selectbox('Select barmode for barchart', barmode_option, key='groping_plot_option', index=barmode_option.index(barmode_default))


        # select True or False for text_auto
        text_auto_option = [True, False]
        text_auto_default = ts_cf['graph_options']['text_auto_default']
        st.selectbox('Select text_auto for barchart', text_auto_option, key='text_auto_option', index=text_auto_option.index(text_auto_default))

def filter_transaction_data(data, segment_filter):

    filtered_data = data.copy()

    # if 'All' is in the segment filter list, do nothing
    if 'All' not in segment_filter:
        filtered_data = filtered_data[filtered_data['segment'].isin(segment_filter)]

    return filtered_data

if 'filter_transaction_data_clicked' not in st.session_state:
    st.session_state.filter_transaction_data_clicked = 0

def filter_transaction_data_button_click():
    st.session_state['filter_transaction_data_clicked'] = 1

# create a button that filteres the data
st.button('Filter Data', key='filter_data_button', on_click=filter_transaction_data_button_click)

if st.session_state.filter_transaction_data_clicked == 1:
    with st.spinner('Filtering data...'):
        st.session_state.transaction_maped_dataset_filtered = filter_transaction_data(st.session_state.transaction_maped_dataset, st.session_state.segment_filter_transactions)
    st.session_state.filter_transaction_data_clicked = 0

if 'transaction_maped_dataset_filtered' not in st.session_state:
    st.session_state.transaction_maped_dataset_filtered = st.session_state.transaction_maped_dataset

@st.cache_resource
def transaction_time_series_by_segment(data, x_column, barmode_option='group', text_auto=True):

    if x_column == 'total':
        data_summary = data.groupby(['segment']).agg(
            quantity=('sales_quantity', 'sum'),
            revenue=('sales_value', 'sum')
        ).reset_index()

        fig_quantity = px.bar(data_summary,y='quantity', color='segment', barmode=barmode_option, text_auto=text_auto)
        fig_revenue = px.bar(data_summary, y='revenue', color='segment', barmode=barmode_option, text_auto=text_auto)

    else:
        data_summary = data.groupby([x_column, 'segment']).agg(
            quantity=('sales_quantity', 'sum'),
            revenue=('sales_value', 'sum')
        ).reset_index()

        fig_quantity = px.bar(data_summary, x=x_column, y='quantity', color='segment', barmode=barmode_option, text_auto=text_auto)
        fig_revenue = px.bar(data_summary, x=x_column, y='revenue', color='segment', barmode=barmode_option, text_auto=text_auto)

    return fig_quantity, fig_revenue

@st.cache_resource
def transaction_time_series_total(data, x_column, barmode_option='group', text_auto=True):

    if x_column == 'total':
        # create a temp column to group by
        data['segment_total'] = 'Segment Total'
        data_summary = data.groupby(['segment_total']).agg(
            quantity=('sales_quantity', 'sum'),
            revenue=('sales_value', 'sum')
        ).reset_index()

        fig_quantity = px.bar(data_summary, y='quantity', barmode=barmode_option, text_auto=text_auto)
        fig_revenue = px.bar(data_summary, y='revenue', barmode=barmode_option, text_auto=text_auto)
    else:
        data_summary = data.groupby([x_column]).agg(
            quantity=('sales_quantity', 'sum'),
            revenue=('sales_value', 'sum')
        ).reset_index()

        fig_quantity = px.bar(data_summary, x=x_column, y='quantity', barmode=barmode_option, text_auto=text_auto)
        fig_revenue = px.bar(data_summary, x=x_column, y='revenue', barmode=barmode_option, text_auto=text_auto)

    return fig_quantity, fig_revenue

# check if the time_series_option_selected is in session state or is none
if 'time_series_option_selected' not in st.session_state or st.session_state.time_series_option_selected is None:
    st.session_state.time_series_option_selected = 'Monthly'
elif 'time_series_option' in st.session_state:
    st.session_state.time_series_option_selected = st.session_state.time_series_option
else:
    st.session_state.time_series_option_selected = 'Monthly'

st.markdown("## Aggregation Level")
options_list = ["Total", "Daily", "Weekly", "Monthly", "Yearly"]
ts_option_default = st.radio("Aggregation Level", options=options_list, label_visibility='collapsed',
                                index= options_list.index(st.session_state.time_series_option_selected), 
                                key='time_series_option', horizontal=True)
st.session_state.time_series_option_selected = ts_option_default

selectedTheme = None

if st.session_state.time_series_option_selected == "Total":
    
    st.markdown("## Total")
    st.write("Here you can see the total number of transactions.")
    total_total_q_plot, total_total_r_plot = transaction_time_series_total(
        st.session_state.transaction_maped_dataset_filtered, 'total', 
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Total Quantity")
    st.plotly_chart(total_total_q_plot, theme=selectedTheme)
    st.markdown("### Total Revenue")
    st.plotly_chart(total_total_r_plot, theme=selectedTheme)
    total_segment_q_plot, total_segment_r_plot = transaction_time_series_by_segment(
        st.session_state.transaction_maped_dataset_filtered, 'total',
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Total Quantity by Segment")
    st.plotly_chart(total_segment_q_plot, theme=selectedTheme)
    st.markdown("### Total Revenue by Segment")
    st.plotly_chart(total_segment_r_plot, theme=selectedTheme)

if st.session_state.time_series_option_selected == "Daily":
    st.markdown("## Daily")
    st.write("Here you can see the daily number of transactions.")
    daily_total_q_plot, daily_total_r_plot = transaction_time_series_total(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_date', 
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Daily Quantity")
    st.plotly_chart(daily_total_q_plot, theme=selectedTheme)
    st.markdown("### Daily Revenue")
    st.plotly_chart(daily_total_r_plot, theme=selectedTheme)
    daily_segment_q_plot, daily_segment_r_plot = transaction_time_series_by_segment(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_date', 
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Daily Quantity by Segment")
    st.plotly_chart(daily_segment_q_plot, theme=selectedTheme)
    st.markdown("### Daily Revenue by Segment")
    st.plotly_chart(daily_segment_r_plot, theme=selectedTheme)

if st.session_state.time_series_option_selected == "Weekly":
    st.markdown("## Weekly")
    st.write("Here you can see the weekly number of transactions.")
    weekly_total_q_plot, weekly_total_r_plot = transaction_time_series_total(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_week_date',
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Weekly Quantity")
    st.plotly_chart(weekly_total_q_plot, theme=selectedTheme)
    st.markdown("### Weekly Revenue")
    st.plotly_chart(weekly_total_r_plot, theme=selectedTheme)
    weekly_segment_q_plot, weekly_segment_r_plot = transaction_time_series_by_segment(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_week_date',
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Weekly Quantity by Segment")
    st.plotly_chart(weekly_segment_q_plot, theme=selectedTheme)
    st.markdown("### Weekly Revenue by Segment")
    st.plotly_chart(weekly_segment_r_plot, theme=selectedTheme)

if st.session_state.time_series_option_selected == "Monthly":
    st.markdown("## Monthly")
    st.write("Here you can see the monthly number of transactions.")
    monthly_total_q_plot, monthly_total_r_plot = transaction_time_series_total(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_month_date',
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Monthly Quantity")
    st.plotly_chart(monthly_total_q_plot, theme=selectedTheme)
    st.markdown("### Monthly Revenue")
    st.plotly_chart(monthly_total_r_plot, theme=selectedTheme)
    monthly_segment_q_plot, monthly_segment_r_plot = transaction_time_series_by_segment(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_month_date',
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Monthly Quantity by Segment")
    st.plotly_chart(monthly_segment_q_plot, theme=selectedTheme)
    st.markdown("### Monthly Revenue by Segment")
    st.plotly_chart(monthly_segment_r_plot, theme=selectedTheme)

if st.session_state.time_series_option_selected == "Yearly":
    st.markdown("## Yearly")
    st.write("Here you can see the yearly number of transactions.")
    yearly_total_q_plot, yearly_total_r_plot = transaction_time_series_total(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_year_date',
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Yearly Quantity")
    st.plotly_chart(yearly_total_q_plot, theme=selectedTheme)
    st.markdown("### Yearly Revenue")
    st.plotly_chart(yearly_total_r_plot, theme=selectedTheme)
    yearly_segment_q_plot, yearly_segment_r_plot = transaction_time_series_by_segment(
        st.session_state.transaction_maped_dataset_filtered, 'transaction_year_date',
        barmode_option=st.session_state.groping_plot_option, text_auto=st.session_state.text_auto_option)
    st.markdown("### Yearly Quantity by Segment")
    st.plotly_chart(yearly_segment_q_plot, theme=selectedTheme)
    st.markdown("### Yearly Revenue by Segment")
    st.plotly_chart(yearly_segment_r_plot, theme=selectedTheme)

  