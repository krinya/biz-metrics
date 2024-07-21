import streamlit as st
import pandas as pd
import numpy as np

from utils.pages_and_titles import *

base_url = 'https://biz-metrics.streamlit.app/'

st.title("Biz-Metrics")
st.subheader("Welcome to Biz-Metrics - a tool to help you understand your business data.")
st.markdown("This is a pilot tool, which means that it is still in development. If you have any feedback or suggestions, please let us know.")

st.subheader("What is Biz-Metrics? What can it do?")
st.markdown(
f"""
Biz-Metrics is an online tool designed to help you understand your business data better, enabling more informed decision-making. 
It allows you to visualize and analyze your data in a simple and intuitive way. By inputting your transaction and user data, Biz-Metrics provides a comprehensive overview of your business using just these two datasets.

Some questions that Biz-Metrics can help you answer:
* **How many users does my business have in total?**
* **How many users did my business interact with in the past period? Is it increasing or decreasing?**
* **How many returning users does my business have?**
* **Which users are the most active?**
* **Which users purchased in the past 30 days? Or which users did not purchase in the past 90 days but purchased before?**
* **Cohort analysis based on the first purchase date for users, transactions, and revenue.**
"""
)

st.subheader("Who is Biz-Metrics useful for?")
st.markdown(
f"""
Biz-Metrics is invaluable for businesses that have collected transaction and user data. 
It helps you gain insights into user behavior and transaction patterns, summarized through KPIs and visualizations.

Biz-Metrics can be particularly beneficial for:
* **Reporting and analytics:** Gain comprehensive reports and dashboards to monitor your business performance.
* **Setting up automated marketing campaigns:** Integrate with marketing automation tools to send targeted emails based on user behavior.
* **Enhancing customer data for different departments:** Provide valuable insights for sales, marketing, customer service, data analytics, and data science teams.
* **Triggering actions based on specific user behaviors:** Automate actions such as sending notifications or alerts when certain user activities are detected.

By leveraging these insights, businesses can optimize their operations, enhance marketing strategies, improve customer engagement, and make more informed decisions.
"""
)

st.subheader("What kind of data do I need to use Biz-Metrics?")
st.markdown(
f"""
Biz-Metrics requires two datasets to provide insights into your business:
* **Transaction data**: This dataset should include information about each transaction, such as the transaction ID, user ID, transaction date, and transaction amount.
* **User data**: This dataset should include information about each user, such as the user ID, registration date, and any other relevant user attributes.
By connecting these two datasets, Biz-Metrics can provide a comprehensive overview of your business performance and user behavior.

There are sample datasets available in the tool that you can use to explore the functionalities of Biz-Metrics.
""")

st.subheader("How to use Biz-Metrics?")
st.markdown("#### Step 1: Import data")
# you can do this on the 'Import Data' page
# as this is a pilot tool there are some sample datasets but you can upload your own transaction data as well
# currentyl registration data is not needed, and therefore the usege of the user data is not implemented everyting is based on the transaction data
st.markdown(
    f"""* Go to the [**Import Data**]({base_url}/import_page) page and choose among the sample datasets or upload your own transaction data.
    (Currently the tool is using only transaction data, and all the statistics are calculated based on that data. Future versions will include user data as well.)""")
st.markdown(
    f"""* Once you selected the dataset that you want to give as input and it is imported, you need to map the columns of the dataset.
    In short, you need to tell which column in your dataset contains what kind of information.
    E.g. which column contains the user_id, transaction_id, transaction_date, etc. This is how the tool can understand your data.
    """)

st.markdown("#### Step 2: View the calculated statistics")
st.markdown(
f"""Once you imported the data and mapped the columns of it, you can navigate to other pages where you can see the statistics of your business.""")

st.subheader(f"""Short description of the pages""")
st.markdown(
f"""
* [**Time Series**]({base_url}/transaction_statistics_time_series): Placeholder for the description of the page
* [**Single User View**]({base_url}/single_user_view): Placeholder for the description of the page
* [**All User View**]({base_url}/all_user_view): Placeholder for the description of the page
* [**User Statistics**]({base_url}/user_statistics): Placeholder for the description of the page
""")





