import pandas as pd
import numpy as np
import streamlit as st

from utils.import_data_functions import * 

def load_sample_data(data):
    if 'dataset2' or 'transaction_maped_dataset' not in st.session_state:
        st.session_state.dataset2, _ = import_data_2()
        user_id_column_defualt = 'Customer ID'
        st.session_state.user_id_column_selected = user_id_column_defualt
        transaction_id_column_defualt = 'Order ID'
        st.session_state.transaction_id_column_selected = transaction_id_column_defualt
        transaction_date_column_defualt = 'Order Date'
        st.session_state.transaction_date_column_selected = transaction_date_column_defualt
        sales_quantity_column_defualt = 'No column is selected'
        st.session_state.sales_quantity_column_selected = sales_quantity_column_defualt
        unit_price_column_defualt = 'No column is selected'
        st.session_state.unit_price_column_selected = unit_price_column_defualt
        sales_value_column_defualt = 'Sales'
        st.session_state.sales_value_column_selected = sales_value_column_defualt
        segment_column_defualt = ['Segment', 'City']
        st.session_state.segment_column_selected = segment_column_defualt
        create_maped_dataset(st.session_state.dataset2)


def check_if_date_is_loaded():
    if 'transaction_maped_dataset' not in st.session_state:
        st.error("Please got the the 'import data' page and map the columns first or you can import a sample here.")
        # create a button that loads the sample data if the user has not imported any data
        # load sample data instead if the user has not imported any data
        st.button("Load Sample Data", on_click=load_sample_data, key="load_sample_data", args=(None,))
        st.stop()

def import_data_1():
    if 'dataset1' not in st.session_state:
        dataset1_path = "sample_datasets/ecommerce_data1.csv"
        dataset1 = pd.read_csv(dataset1_path).convert_dtypes()
        st.session_state.dataset1 = dataset1
        st.session_state.dataset1_shape = dataset1.shape
    return st.session_state.dataset1, st.session_state.dataset1_shape


def import_data_2():
    if 'dataset2' not in st.session_state:
        dataset2_path = "sample_datasets/ecommerce_data2.csv"
        dataset2 = pd.read_csv(dataset2_path).convert_dtypes()
        st.session_state.dataset2 = dataset2
        st.session_state.dataset2_shape = dataset2.shape
    return st.session_state.dataset2, st.session_state.dataset2_shape

def import_data_3():
    if 'dataset3' not in st.session_state:
        dataset3_path = "sample_datasets/ecommerce_data3.csv"
        dataset3 = pd.read_csv(dataset3_path, encoding='latin1').convert_dtypes()
        st.session_state.dataset3 = dataset3
        st.session_state.dataset3_shape = dataset3.shape
    return st.session_state.dataset3, st.session_state.dataset3_shape


def create_maped_dataset(dataset):
        
        user_id_column = st.session_state.user_id_column_selected
        invoice_id_column = st.session_state.transaction_id_column_selected
        transaction_date_column = st.session_state.transaction_date_column_selected
        sales_quantity_column = st.session_state.sales_quantity_column_selected
        unit_price_column = st.session_state.unit_price_column_selected
        sales_amount_column = st.session_state.sales_value_column_selected
        segment_column = st.session_state.segment_column_selected

        with st.spinner("Mapping the columns of the dataset..."):

            st.session_state.transaction_maped_dataset = pd.DataFrame()

            if user_id_column != 'No column is selected':
                st.session_state.transaction_maped_dataset['user_id'] = dataset[user_id_column]
                # convert it to a string
                st.session_state.transaction_maped_dataset['user_id'] = st.session_state.transaction_maped_dataset['user_id'].astype(str)
            if user_id_column == 'No column is selected':
                st.session_state.transaction_maped_dataset['user_id'] = 'unknown user'

            if invoice_id_column != 'No column is selected':
                st.session_state.transaction_maped_dataset['invoice_id'] = dataset[invoice_id_column]
                # convert it to a string
                st.session_state.transaction_maped_dataset['invoice_id'] = st.session_state.transaction_maped_dataset['invoice_id'].astype(str)

            if transaction_date_column != 'No column is selected':
                st.session_state.transaction_maped_dataset['transaction_date_time'] = dataset[transaction_date_column]
                # convert it to datetime
                st.session_state.transaction_maped_dataset['transaction_date_time'] = pd.to_datetime(st.session_state.transaction_maped_dataset['transaction_date_time'], errors='coerce')
                # convert it to date
                st.session_state.transaction_maped_dataset['transaction_date'] = st.session_state.transaction_maped_dataset['transaction_date_time'].dt.date
                # convert it to date week start date
                st.session_state.transaction_maped_dataset['transaction_week_date'] = st.session_state.transaction_maped_dataset['transaction_date_time'].dt.to_period('W').apply(lambda r: r.start_time.date())
                # convert it to date month start date
                st.session_state.transaction_maped_dataset['transaction_month_date'] = st.session_state.transaction_maped_dataset['transaction_date_time'].dt.to_period('M').apply(lambda r: r.start_time.date())
                # convert it to date quarter start date
                st.session_state.transaction_maped_dataset['transaction_quarter_date'] = st.session_state.transaction_maped_dataset['transaction_date_time'].dt.to_period('Q').apply(lambda r: r.start_time.date())
                # convert it to date year start date
                st.session_state.transaction_maped_dataset['transaction_year_date'] = st.session_state.transaction_maped_dataset['transaction_date_time'].dt.to_period('Y').apply(lambda r: r.start_time.date())


            if sales_quantity_column != 'No column is selected':
                st.session_state.transaction_maped_dataset['sales_quantity'] = dataset[sales_quantity_column]
                # convert it to numeric
                st.session_state.transaction_maped_dataset['sales_quantity'] = pd.to_numeric(st.session_state.transaction_maped_dataset['sales_quantity'], errors='coerce')
            if sales_quantity_column == 'No column is selected':
                st.session_state.transaction_maped_dataset['sales_quantity'] = 1
                # convert it to numeric
                st.session_state.transaction_maped_dataset['sales_quantity'] = pd.to_numeric(st.session_state.transaction_maped_dataset['sales_quantity'], errors='coerce')

            if unit_price_column != 'No column is selected':
                st.session_state.transaction_maped_dataset['unit_price'] = dataset[unit_price_column]
                # convert it to numeric
                st.session_state.transaction_maped_dataset['unit_price'] = pd.to_numeric(st.session_state.transaction_maped_dataset['unit_price'], errors='coerce')
            if unit_price_column == 'No column is selected':
                st.session_state.transaction_maped_dataset['unit_price'] = 1
                # convert it to numeric
                st.session_state.transaction_maped_dataset['unit_price'] = pd.to_numeric(st.session_state.transaction_maped_dataset['unit_price'], errors='coerce')

            if sales_amount_column != 'No column is selected':
                st.session_state.transaction_maped_dataset['sales_value'] = dataset[sales_amount_column]
                # convert it to numeric
                st.session_state.transaction_maped_dataset['sales_value'] = pd.to_numeric(st.session_state.transaction_maped_dataset['sales_value'], errors='coerce')
            if sales_amount_column == 'No column is selected':
                st.session_state.transaction_maped_dataset['sales_value'] = 1

            # segment_column is ['No column is selected'] or ['column_name'] or is None
            if segment_column != ['No column is selected'] or segment_column != [] or segment_column != None:
                # concatenate the selected columns into one column
                st.session_state.transaction_maped_dataset['segment'] = dataset[segment_column].apply(lambda x: ' - '.join(x.dropna().astype(str)), axis=1)
            if segment_column == ['No column is selected'] or segment_column == [] or segment_column == None:
                st.session_state.transaction_maped_dataset['segment'] = 'All Segments'

            # if unit_price_column not 'No column is selected' and sales_quantity_column not 'No column is selected' then calculate the sales_value
            if unit_price_column != 'No column is selected' and sales_quantity_column != 'No column is selected':
                st.session_state.transaction_maped_dataset['sales_value'] = st.session_state.transaction_maped_dataset['unit_price'] * st.session_state.transaction_maped_dataset['sales_quantity']
            if unit_price_column == 'No column is selected' and sales_quantity_column == 'No column is selected':
                st.session_state.transaction_maped_dataset['unit_price'] = st.session_state.transaction_maped_dataset['sales_value']