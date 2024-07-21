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
sus_cf = read_config(section = 'all_user_view')

st.title("Single User View")
st.markdown("Here you can see some statistics about one users.")

st.session_state.transaction_maped_dataset = check_if_data_is_loaded(get_session_id())

st.markdown("### Filter transaction data")
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

st.markdown("### Filter using the sliders and multiselects")

# list all columns except user_id
cols_to_create_filter_for = st.session_state.total_users_summary_data_filtered.columns.tolist()
cols_to_create_filter_for.remove('user_id')
# get the col type of the columns 
# create filters in streamlit

number_of_columns = 4
i = 0
col_to_render = st.columns(number_of_columns)
filter_keys_dict = {}

for col in cols_to_create_filter_for:
    # get the type of the column
    col_type = st.session_state.total_users_summary_data_filtered[col].dtype
    # if col type is int or float then create a min max slider
    if col_type == np.int64 or col_type == np.float64:
        min_value = st.session_state.total_users_summary_data_filtered[col].min()
        max_value = st.session_state.total_users_summary_data_filtered[col].max()
        filter_key = f'{col}_filter_key'
        if min_value == max_value:
            st_slider_arguments = dict(label=col, value=[min_value, max_value+1],  min_value=min_value, max_value=max_value+1, key=filter_key)
        else:
            st_slider_arguments = dict(label=col, value=[min_value, max_value+1], min_value=min_value, max_value=max_value, key=filter_key)
        # add it to the filter_key_dict with the key as the column name and type as the column type
        filter_keys_dict[col] = {'type': col_type, 'key': filter_key}
        col_positon = i % number_of_columns
        with col_to_render[col_positon]:
            st.slider(**st_slider_arguments)
            # createa s hisogram using plotly and set the hight to 100 set min value on x axis to min value and max value to max value
            hight_of_hisogram = 100
            fig = px.histogram(st.session_state.total_users_summary_data_filtered, x=col, height=hight_of_hisogram)
            fig.update_xaxes(range=[min_value, max_value])
            # do not show the y axis and x axis name but show the values
            fig.update_yaxes(title_text='')
            # do not show x axis name
            fig.update_xaxes(title_text='')
            # set the margin to 0
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            
            
            st.plotly_chart(fig, use_container_width=True, hight=hight_of_hisogram)
        i += 1

    if col_type == np.dtype('O'):
        unique_values = st.session_state.total_users_summary_data_filtered[col].unique()
        # all 'All' to the unique values to the beginning of the list
        unique_values = np.insert(unique_values, 0, 'All')
        # make default to 'All'
        filter_key = f'{col}_filter_key'
        st_multiselect_arguments = dict(label=col, options=unique_values, default=['All'], key=filter_key)
        # add it to the filter_key_dict with the key as the column name and type as the column type
        filter_keys_dict[col] = {'type': col_type, 'key': filter_key}
        col_positon = i % number_of_columns
        with col_to_render[col_positon]:
            st.multiselect(**st_multiselect_arguments)
        i += 1
        

def filter_multi_user_data(data, filter_keys_dict):
    # filter the data
    for key in filter_keys_dict.keys():
        col_type = filter_keys_dict[key]['type']
        filter_key = filter_keys_dict[key]['key']
        if col_type == np.int64 or col_type == np.float64:
            min_value, max_value = st.session_state[filter_key]
            data = data[(data[key] >= min_value) & (data[key] <= max_value)]
        if col_type == np.dtype('O'):
            selected_values = st.session_state[filter_key]
            if 'All' not in selected_values:
                data = data[data[key].isin(selected_values)]

    st.session_state.total_users_summary_data_filtered_sliders = data
    return st.session_state.total_users_summary_data_filtered_sliders

# create a button that filteres the data
st.button('Apply filters', key='filter_data_button_slider', on_click=filter_multi_user_data,
          args=(st.session_state.total_users_summary_data_filtered, filter_keys_dict))

if 'total_users_summary_data_filtered_sliders' not in st.session_state:
    st.session_state.total_users_summary_data_filtered_sliders = filter_multi_user_data(st.session_state.total_users_summary_data_filtered, filter_keys_dict)

st.markdown("## Users' data after filtering")
st.dataframe(st.session_state.total_users_summary_data_filtered_sliders.set_index('user_id'), use_container_width=True, selection_mode="single-row")
# write the shape
st.markdown(f"Number of users in the filtered_data: #{st.session_state.total_users_summary_data_filtered_sliders.shape[0]}")