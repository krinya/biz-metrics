import streamlit as st
import pandas as pd
import numpy as np

from utils.pages_and_titles import *

st.title("Import")
st.write("Here you can select from the sample datasets or upload your own dataset.")

st.markdown("## Sample Datasets")

tab1, tab2, tab3, tab_own = st.tabs(["Sample Dataset 1", "Sample Dataset 2", "Sample Dataset 3", "Own Data"])

def select_dataset_button_press(dataset_name):
    st.session_state.selected_row_data = st.session_state[dataset_name]
    st.session_state.dataset_name = dataset_name

def selected_dataset_column_mapping(dataset):

    colnames_in_the_dataset = dataset.columns
    coltypes_in_the_dataset = dataset.dtypes

    df_with_colnames_and_coltypes = pd.DataFrame({'Column Name': colnames_in_the_dataset, 'Column Type': coltypes_in_the_dataset})

    return df_with_colnames_and_coltypes, colnames_in_the_dataset, coltypes_in_the_dataset

with tab1:
    if 'dataset1' not in st.session_state:
        dataset1_path = "sample_datasets/ecommerce_data1.csv"
        dataset1 = pd.read_csv(dataset1_path)
        st.session_state.dataset1 = dataset1
        st.session_state.dataset1_shape = dataset1.shape
    st.dataframe(st.session_state.dataset1 , use_container_width=True, hide_index=True)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write(f"Dataset has: {st.session_state.dataset1_shape[0]} rows, {st.session_state.dataset1_shape[1]} columns")
    with col3:
        st.download_button("Download Dataset 1", data=st.session_state.dataset1.to_csv(index=False), file_name='ecommerce_data1.csv', mime='text/csv', key='download_button_ds1')
    st.button("Select this dataset", on_click=select_dataset_button_press, args=('dataset1', ), key='dataset1_button')

with tab2:
    if 'dataset2' not in st.session_state:
        dataset2_path = "sample_datasets/ecommerce_data2.csv"
        dataset2 = pd.read_csv(dataset2_path)
        st.session_state.dataset2 = dataset2
        st.session_state.dataset2_shape = dataset2.shape
    st.dataframe(st.session_state.dataset2, use_container_width=True, hide_index=True)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write(f"Dataset has: {st.session_state.dataset2_shape[0]} rows, {st.session_state.dataset2_shape[1]} columns")
    with col3:
        st.download_button("Download Dataset 2", data=st.session_state.dataset2.to_csv(index=False), file_name='ecommerce_data2.csv', mime='text/csv', key='download_button_ds2')
    st.button("Select this dataset", on_click=select_dataset_button_press, args=('dataset2', ), key='dataset2_button')

with tab3:
    if 'dataset3' not in st.session_state:
        dataset3_path = "sample_datasets/ecommerce_data3.csv"
        dataset3 = pd.read_csv(dataset3_path, encoding='latin1')
        st.session_state.dataset3 = dataset3
        st.session_state.dataset3_shape = dataset3.shape
    st.dataframe(st.session_state.dataset3, use_container_width=True, hide_index=True)
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        st.write(f"Dataset has: {st.session_state.dataset3_shape[0]} rows, {st.session_state.dataset3_shape[1]} columns")
    with col3:
        st.download_button("Download Dataset 3", data=st.session_state.dataset3.to_csv(index=False), file_name='ecommerce_data3.csv', mime='text/csv', key='download_button_ds3')
    st.button("Select this dataset", on_click=select_dataset_button_press, args=('dataset3', ), key='dataset3_button')

with tab_own:
    uploaded_file = st.file_uploader("Upload your own dataset", type=['csv'])
    if uploaded_file is not None:
        if 'own_data' not in st.session_state:
            own_data = pd.read_csv(uploaded_file)
            st.session_state.own_data = own_data
            st.session_state.own_data_shape = own_data.shape
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
if 'selected_row_data' in st.session_state:
    # write the name of the dataset
    name_of_dataset = st.session_state.selected_row_data
    st.markdown(f"### You selected the following dataset: {st.session_state.dataset_name}")
    #st.dataframe(st.session_state.selected_row_data, use_container_width=True, hide_index=True)

    # Map the columns
    st.markdown("### Map the columns of the dataset to the required columns")
    column_mapping_df, colnames_in_the_dataset, coltypes_in_the_dataset = selected_dataset_column_mapping(st.session_state.selected_row_data)
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

    def create_maped_dataset(dataset):

        user_id_column = st.session_state.user_id_column_selected
        st.write(user_id_column)
        invoice_id_column = st.session_state.transaction_id_column_selected
        transaction_date_column = st.session_state.transaction_date_column_selected
        sales_quantity_column = st.session_state.sales_quantity_column_selected
        unit_price_column = st.session_state.unit_price_column_selected
        sales_amount_column = st.session_state.sales_value_column_selected
        segment_column = st.session_state.segment_column_selected

        with st.spinner("Creating mapped dataset..."):

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


    # create the mapped dataset using a button
    if st.button("Create Mapped Dataset"):
        create_maped_dataset(st.session_state.selected_row_data)
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