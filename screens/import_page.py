import streamlit as st
import pandas as pd
import numpy as np

from utils.pages_and_titles import *
from utils.import_data_functions import *
from utils.create_session_id import *
session_id = get_session_id()

st.title("Import")
st.write("Here you can select from the sample datasets or upload your own dataset.")

st.markdown("## Sample Datasets")

def select_dataset_button_press(dataset_name):
    st.session_state.selected_raw_data = st.session_state[dataset_name]
    st.session_state.dataset_name = dataset_name

def selected_dataset_column_mapping(dataset):

    colnames_in_the_dataset = dataset.columns
    coltypes_in_the_dataset = dataset.dtypes

    df_with_colnames_and_coltypes = pd.DataFrame({'Column Name': colnames_in_the_dataset, 'Column Type': coltypes_in_the_dataset})

    return df_with_colnames_and_coltypes, colnames_in_the_dataset, coltypes_in_the_dataset

dataset_selectbox_options_list = ["Sample Dataset 1", "Sample Dataset 2", "Sample Dataset 3", "Own Data"]
if 'selected_dataset_selectbox_options' not in st.session_state:
    st.session_state.selected_dataset_selectbox_options = dataset_selectbox_options_list[0]
st.selectbox("Select a dataset", dataset_selectbox_options_list,
             key='dataset_selectbox_options',
             index=dataset_selectbox_options_list.index(st.session_state.selected_dataset_selectbox_options))
st.session_state.selected_dataset_selectbox_options = st.session_state.dataset_selectbox_options


if st.session_state.dataset_selectbox_options == "Sample Dataset 1":
    if 'dataset1' not in st.session_state:
        import_data_1(session_id)
        
    st.dataframe(st.session_state.dataset1 , use_container_width=True, hide_index=True)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write(f"Dataset has: {st.session_state.dataset1_shape[0]} rows, {st.session_state.dataset1_shape[1]} columns")
    with col3:
        st.download_button("Download Dataset 1", data=st.session_state.dataset1.to_csv(index=False), file_name='ecommerce_data1.csv', mime='text/csv', key='download_button_ds1')
    st.button("Select this dataset", on_click=select_dataset_button_press, args=('dataset1', ), key='dataset1_button')

if st.session_state.dataset_selectbox_options == "Sample Dataset 2":
    if 'dataset2' not in st.session_state:
        import_data_2(session_id)

    st.dataframe(st.session_state.dataset2, use_container_width=True, hide_index=True)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write(f"Dataset has: {st.session_state.dataset2_shape[0]} rows, {st.session_state.dataset2_shape[1]} columns")
    with col3:
        st.download_button("Download Dataset 2", data=st.session_state.dataset2.to_csv(index=False), file_name='ecommerce_data2.csv', mime='text/csv', key='download_button_ds2')
    st.button("Select this dataset", on_click=select_dataset_button_press, args=('dataset2', ), key='dataset2_button')

if st.session_state.dataset_selectbox_options == "Sample Dataset 3":
    if 'dataset3' not in st.session_state:
        import_data_3(session_id)

    st.dataframe(st.session_state.dataset3, use_container_width=True, hide_index=True)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write(f"Dataset has: {st.session_state.dataset3_shape[0]} rows, {st.session_state.dataset3_shape[1]} columns")
    with col3:
        st.download_button("Download Dataset 3", data=st.session_state.dataset3.to_csv(index=False), file_name='ecommerce_data3.csv', mime='text/csv', key='download_button_ds3')
    st.button("Select this dataset", on_click=select_dataset_button_press, args=('dataset3', ), key='dataset3_button')

def read_in_uploaded_file():
    if st.session_state.own_uploaded_file is None:
        return
    own_data = pd.read_csv(st.session_state.own_uploaded_file).convert_dtypes()
    st.session_state.own_data = own_data
    st.session_state.own_data_shape = own_data.shape

if st.session_state.dataset_selectbox_options == "Own Data":
    uploaded_file = st.file_uploader("Upload your own dataset", type=['csv'], key='own_uploaded_file', on_change=read_in_uploaded_file)
            
    if 'own_data' in st.session_state:
        st.dataframe(st.session_state.own_data, use_container_width=True, hide_index=True)
        col1, col2, col3 = st.columns([2, 4, 2])
        with col1:
            st.write(f"Dataset has: {st.session_state.own_data_shape[0]} rows, {st.session_state.own_data_shape[1]} columns")
        with col3:
            st.download_button("Download Own Dataset", data=st.session_state.own_data.to_csv(index=False), file_name='own_data.csv', mime='text/csv', key='download_button_own_data')
        st.button("Select this dataset", on_click=select_dataset_button_press, args=('own_data', ), key='own_data_button')
    else:
        st.markdown("Please upload a dataset.")

st.markdown("---")

st.markdown("## Selected Data")
if 'selected_raw_data' in st.session_state:
    # write the name of the dataset
    name_of_dataset = st.session_state.selected_raw_data
    st.markdown(f"### You selected the following dataset: {st.session_state.dataset_name}")
    #st.dataframe(st.session_state.selected_raw_data, use_container_width=True, hide_index=True)

    # Map the columns
    st.markdown("### Map the columns of the dataset to the required columns")
    column_mapping_df, colnames_in_the_dataset, coltypes_in_the_dataset = selected_dataset_column_mapping(st.session_state.selected_raw_data)
    #st.dataframe(column_mapping_df, use_container_width=True, hide_index=True)

    if st.session_state.dataset_name == 'dataset1':
        st.markdown("You selected dataset1 here I already maped the columns for you, but if you would like to change someting you can do it.")
        user_id_column_defualt = 'Customer type'
        transaction_id_column_defualt = 'Invoice ID'
        transaction_date_column_defualt = 'Date'
        sales_quantity_column_defualt = 'Quantity'
        unit_price_column_defualt = 'Unit price'
        sales_value_column_defualt = 'No column is selected'
        segment_column_defualt = ['Branch', 'City']
    elif st.session_state.dataset_name == 'dataset2':
        st.markdown("You selected dataset2 here I already maped the columns for you, but if you would like to change someting you can do it.")
        user_id_column_defualt = 'Customer ID'
        transaction_id_column_defualt = 'Order ID'
        transaction_date_column_defualt = 'Order Date'
        sales_quantity_column_defualt = 'No column is selected'
        unit_price_column_defualt = 'No column is selected'
        sales_value_column_defualt = 'Sales'
        segment_column_defualt = ['Segment', 'City']
    elif st.session_state.dataset_name == 'dataset3':
        st.markdown("You selected dataset3 here I already maped the columns for you, but if you would like to change someting you can do it.")
        user_id_column_defualt = 'CustomerID'
        transaction_id_column_defualt = 'InvoiceNo'
        transaction_date_column_defualt = 'InvoiceDate'
        sales_quantity_column_defualt = 'Quantity'
        unit_price_column_defualt = 'UnitPrice'
        sales_value_column_defualt = 'No column is selected'
        segment_column_defualt = ['Country']
    else:
        st.markdown("You selected your own dataset, please map the columns to the required columns.")
        user_id_column_defualt = 'No column is selected'
        transaction_id_column_defualt = 'No column is selected'
        transaction_date_column_defualt = 'No column is selected'
        sales_quantity_column_defualt = 'No column is selected'
        unit_price_column_defualt = 'No column is selected'
        sales_value_column_defualt = 'No column is selected'
        segment_column_defualt = None

    # add 'no column is selected' to the colnames_in_the_dataset and put it to the first place
    colnames_in_the_dataset = ['No column is selected'] + list(colnames_in_the_dataset)

    st.markdown("### Select User ID column")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.selectbox("Select User ID column", colnames_in_the_dataset, key='user_id_column_selected', index=colnames_in_the_dataset.index(user_id_column_defualt))

    st.markdown("### Select Transaction ID column")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.selectbox("Select Transaction ID column", colnames_in_the_dataset, key='transaction_id_column_selected', index=colnames_in_the_dataset.index(transaction_id_column_defualt))

    st.markdown("### Select Transaction date column")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.selectbox("Select Transaction date column", colnames_in_the_dataset, key='transaction_date_column_selected', index=colnames_in_the_dataset.index(transaction_date_column_defualt))

    st.markdown("### Select Sales Quantity column")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.selectbox("Select Sales Quantity column", colnames_in_the_dataset, key='sales_quantity_column_selected', index=colnames_in_the_dataset.index(sales_quantity_column_defualt))
    
    st.markdown("### Select Unit Price column")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.selectbox("Select Unit Price column", colnames_in_the_dataset, key='unit_price_column_selected', index=colnames_in_the_dataset.index(unit_price_column_defualt))

    st.markdown("### Select Sales Value column")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.selectbox("Select Sales Value column", colnames_in_the_dataset, key='sales_value_column_selected', index=colnames_in_the_dataset.index(sales_value_column_defualt))

    st.markdown("### Select Segment column(s)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.multiselect("Select Segment column(s)", options=colnames_in_the_dataset, key='segment_column_selected', placeholder='Select one or more columns', default=segment_column_defualt)

    # create the mapped dataset using a button
    if st.button("Create Mapped Dataset"):
        if st.session_state.dataset_name == 'dataset2':
            data_format_input = "%d/%m/%Y"
        else:
            data_format_input = None
        create_maped_dataset(st.session_state.selected_raw_data, date_format=data_format_input)
        st.success("Mapped dataset has been created. You can see it below.")
        st.session_state.transaction_maped_dataset_shape = st.session_state.transaction_maped_dataset.shape
    
    st.markdown("### Mapped Dataset")
    if 'transaction_maped_dataset' in st.session_state:
        st.dataframe(st.session_state.transaction_maped_dataset, use_container_width=True, hide_index=True)
        col1, col2, col3 = st.columns([2, 4, 2])
        with col1:
            st.write(f"Dataset has: {st.session_state.transaction_maped_dataset_shape[0]} rows, {st.session_state.transaction_maped_dataset_shape[1]} columns")
        with col3:
            st.download_button("Download Mapped Dataset", data=st.session_state.transaction_maped_dataset.to_csv(index=False), file_name='transaction_maped_dataset.csv', mime='text/csv', key='download_button_transaction_maped_dataset')
    else:
        st.markdown("Please create the mapped dataset.")

else:
    st.markdown("Please select a dataset.")