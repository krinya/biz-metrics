import streamlit as st
import pandas as pd
import numpy as np

from utils.pages_and_titles import *
from utils.import_data_functions import *

st.title("Sample Datasets")
st.write("Here you can see some sample datasets.")
st.markdown("## Transaction Samples")

st.markdown("### Dataset 1")
if 'dataset1' not in st.session_state:
    import_data_1()

st.dataframe(st.session_state.dataset1, use_container_width=True, hide_index=True)
st.write(f"Shape of the dataset: {st.session_state.dataset1_shape}")
st.download_button("Download Dataset 1", data=st.session_state.dataset1.to_csv(index=False), file_name='ecommerce_data1.csv', mime='text/csv')

st.markdown("### Dataset 2")
if 'dataset2' not in st.session_state:
    import_data_2()

st.dataframe(st.session_state.dataset2, use_container_width=True, hide_index=True)
st.write(f"Shape of the dataset: {st.session_state.dataset2_shape}")
st.download_button("Download Dataset 2", data=st.session_state.dataset2.to_csv(index=False), file_name='ecommerce_data2.csv', mime='text/csv')

st.markdown("### Dataset 3")
if 'dataset3' not in st.session_state:
    import_data_3()

st.dataframe(st.session_state.dataset3, use_container_width=True, hide_index=True)
shape_of_dataset3 = st.session_state.dataset3.shape
st.write(f"Shape of the dataset: {st.session_state.dataset3_shape}")
st.download_button("Download Dataset 3", data=st.session_state.dataset3.to_csv(index=False), file_name='ecommerce_data3.csv', mime='text/csv')