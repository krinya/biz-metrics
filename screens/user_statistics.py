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

# read the config file
config_all = read_config()
general = read_config(section = 'general')
us_cf = read_config(section = 'user_statistics')
show_sales_triangles_data = us_cf['show_sales_trinangles_data_default']
show_sales_triangels_graph = us_cf['show_sales_tringales_graph_default']

st.title("User Statistics")
st.markdown("Here you can see some statistics about the users.")

st.session_state.transaction_maped_dataset = check_if_data_is_loaded(get_session_id())

sidebar_empty_space = st.sidebar.empty()
sidebar_empty_space.markdown(" ")

if us_cf['developer_mode']:
    st.markdown("## transaction_maped_dataset - Raw Data")
    st.dataframe(st.session_state.transaction_maped_dataset, use_container_width=True, hide_index=True)


def cummulative_users_calculation(data, aggregation_level = 'day', lookback = 30):

    min_date = data['transaction_date'].min()
    max_date = data['transaction_date'].max()
    diff_max_min_date_in_days = (max_date - min_date).days

    # create a date range with all the days between the min and max date
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    with sidebar_empty_space:
        progress_bar_cummulative_users = st.progress(0, text='Calculating cummulative users... Please wait.')

    # create a dataframe with the total unique users until that day who we interacted with
    cummulative_users_df = pd.DataFrame()
    i = 0
    for date in date_range:
        pb_value = i / diff_max_min_date_in_days
        progress_bar_cummulative_users.progress(pb_value, text=f'Calculating cummulative users... {i}/{diff_max_min_date_in_days} days processed.')

        date = pd.Timestamp(date)
        date_minus_lookback = date - pd.DateOffset(days=lookback)

        data_filtered_cummulative = data[data['transaction_date_time'] <= date]
        unique_users_to_date = data_filtered_cummulative['user_id'].nunique()

        data_filtered_lookback = data_filtered_cummulative[data_filtered_cummulative['transaction_date_time'] >= date_minus_lookback]
        unique_users_lookback = data_filtered_lookback['user_id'].nunique()

        cummulative_users_until_date = pd.DataFrame({'date': [date],
                                                     'day': [i + 1],
                                                     'users_to_date': [unique_users_to_date],
                                                     'users_lookback': [unique_users_lookback]})
        
        cummulative_users_df = pd.concat([cummulative_users_df, cummulative_users_until_date], ignore_index=True)

        i += 1

    # convert date to date
    cummulative_users_df['date'] = pd.to_datetime(cummulative_users_df['date']).dt.date

    return cummulative_users_df


def calculating_user_types(data, aggg_level = 'day', lookback_periods = [30, 60], churning_period = 90, until='max_date'):

    min_date = data['transaction_date'].min()
    if until == 'max_date':
        max_date = data['transaction_date'].max()
    if until == 'today':
        max_date = pd.Timestamp.today().date()

    diff_max_min_date_in_days = (max_date - min_date).days

    # create churning_date by adding churning_period to the data['transaction_date']
    data['churning_date'] = data['transaction_date'] + pd.DateOffset(days=churning_period)
    # convert it to date
    data['churning_date'] = pd.to_datetime(data['churning_date']).dt.date
    #st.dataframe(data, use_container_width=True, hide_index=True)

    # create a date range with all the days between the min and max date
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')

    with sidebar_empty_space:
        progress_bar_user_types = st.progress(0, text='Calculating user types... Please wait.')

    # create an empty dataframe where we will store the results
    user_types_df = pd.DataFrame()

    empty_space = st.empty()

    i = 0
    for date in date_range:

        pb_value = i / diff_max_min_date_in_days
        progress_bar_user_types.progress(pb_value, text=f'Calculating user types... {i}/{diff_max_min_date_in_days} days processed.')

        date = pd.Timestamp(date)
        lookback_period_2_date = date - pd.DateOffset(days=lookback_periods[1])
        lookback_period_1_date = date - pd.DateOffset(days=lookback_periods[0])
        date_plus_churning_period = date + pd.DateOffset(days=churning_period)
        date_plus_churning_period_date = pd.Timestamp(date_plus_churning_period).date()
        # st.write(f"Date: {date}, Lookback period 2: {lookback_period_2_date}, Lookback period 1: {lookback_period_1_date}, Churning period: {date_plus_churning_period}")

        df_before_lookback_period = data[data['transaction_date_time'] < lookback_period_2_date]
        
        df_lookback_period_12 = data[(data['transaction_date_time'] >= lookback_period_2_date) & (data['transaction_date_time'] <= date)]
        df_lookback_period_1 = data[(data['transaction_date_time'] >= lookback_period_2_date) & (data['transaction_date_time'] <= lookback_period_1_date)]
        df_lookback_period_2 = data[(data['transaction_date_time'] >= lookback_period_1_date) & (data['transaction_date_time'] <= date)]
        df_churning_period = data[(data['transaction_date_time'] > date) & (data['transaction_date_time'] <= date_plus_churning_period)]
        df_churning_period_min_by_user = df_churning_period.groupby('user_id').agg(
            transaction_date_time = ('transaction_date_time', 'min')
        ).reset_index()

        # filter for the churning period where the churning_date is less than the date_plus_churning_period
        df_churning_period_90 = pd.merge(df_lookback_period_12,
                                         df_churning_period_min_by_user[['user_id', 'transaction_date_time']].rename(columns={'transaction_date_time': 'transaction_date_time_churning'}),
                                         on='user_id', how='inner')
        # calculate day difference between the transaction_date and the transaction_date_churning
        df_churning_period_90['day_difference_churning'] = (df_churning_period_90['transaction_date_time_churning'] - df_churning_period_90['transaction_date_time']).dt.days
        # keep only the rows where the day_difference_churning is less than churning_period
        df_churning_period_90 = df_churning_period_90[df_churning_period_90['day_difference_churning'] <= churning_period]
        
        # calculate user types:
        # - new_users: only present in the lookback period 2 and not in lookback period 1 and not before
        # - returnin_users: present in the lookback period 1 and 2
        # - rare_users: present in the lookback period 2 but not in the lookback period 1 and not new user
        # - potentialy_churning users: present in the lookback period 1 but not in the lookback period 2 and not new user

        new_users_df = df_lookback_period_2[~df_lookback_period_2['user_id'].isin(df_lookback_period_1['user_id']) & ~df_lookback_period_2['user_id'].isin(df_before_lookback_period['user_id'])]
        new_users_count = new_users_df['user_id'].nunique()
        returning_users_df = df_lookback_period_1[df_lookback_period_1['user_id'].isin(df_lookback_period_2['user_id'])]
        returning_users_count = returning_users_df['user_id'].nunique()
        rare_users_df = df_lookback_period_2[~df_lookback_period_2['user_id'].isin(df_lookback_period_1['user_id']) & ~df_lookback_period_2['user_id'].isin(new_users_df['user_id'])]
        rare_users_count = rare_users_df['user_id'].nunique()
        potentially_churning_users_df = df_lookback_period_1[~(df_lookback_period_1['user_id'].isin(df_lookback_period_2['user_id'])) & ~(df_lookback_period_1['user_id'].isin(new_users_df['user_id']))]
        potentially_churning_users_count = potentially_churning_users_df['user_id'].nunique()

        # calculate churning users and churn rate for each user type
        new_user_churn_df = new_users_df[~new_users_df['user_id'].isin(df_churning_period_90['user_id'])]
        new_user_churn_count = new_user_churn_df['user_id'].nunique()
        returning_user_churn_df = returning_users_df[~returning_users_df['user_id'].isin(df_churning_period_90['user_id'])]
        returning_user_churn_count = returning_user_churn_df['user_id'].nunique()
        rare_user_churn_df = rare_users_df[~rare_users_df['user_id'].isin(df_churning_period_90['user_id'])]
        rare_user_churn_count = rare_user_churn_df['user_id'].nunique()
        potentially_churning_user_churn_df = potentially_churning_users_df[~potentially_churning_users_df['user_id'].isin(df_churning_period_90['user_id'])]
        potentially_churning_user_churn_count = potentially_churning_user_churn_df['user_id'].nunique()

        user_types_until_date = pd.DataFrame(
            {
                "date": [date],
                "day": [i + 1],
                "new_users": [new_users_count],
                "returning_users": [returning_users_count],
                "rare_users": [rare_users_count],
                "potentially_churning_users": [potentially_churning_users_count],
                "new_users_churn": [new_user_churn_count],
                "returning_users_churn": [returning_user_churn_count],
                "rare_users_churn": [rare_user_churn_count],
                "potentially_churning_users_churn": [potentially_churning_user_churn_count]
            }
        )

        # fill NaN values with -1
        #user_types_until_date = user_types_until_date.fillna(-1)

        # calculate churn rate make sure that we do not divide by zero
        user_types_until_date['new_users_churn_rate'] = user_types_until_date['new_users_churn'] / user_types_until_date['new_users'].replace(0, np.nan)
        user_types_until_date['returning_users_churn_rate'] = user_types_until_date['returning_users_churn'] / user_types_until_date['returning_users'].replace(0, np.nan)
        user_types_until_date['rare_users_churn_rate'] = user_types_until_date['rare_users_churn'] / user_types_until_date['rare_users'].replace(0, np.nan)
        user_types_until_date['potentially_churning_users_churn_rate'] = user_types_until_date['potentially_churning_users_churn'] / user_types_until_date['potentially_churning_users'].replace(0, np.nan)

        user_types_df = pd.concat([user_types_df, user_types_until_date], ignore_index=True)

        i += 1
    
    # convert date to date
    user_types_df['date'] = pd.to_datetime(user_types_df['date']).dt.date

    return user_types_df

def sales_triangles_calculation(data, aggregation_level = 'day'):

    with st.spinner("Calculating sales triangles... Please wait."):

        if aggregation_level == 'day':
            aggregation_level_column = 'transaction_date'
        if aggregation_level == 'week':
            aggregation_level_column = 'transaction_week_date'
        if aggregation_level == 'month':
            aggregation_level_column = 'transaction_month_date'
        if aggregation_level == 'quarter':
            aggregation_level_column = 'transaction_quarter_date'
        if aggregation_level == 'year':
            aggregation_level_column = 'transaction_year_date'

        from_date = data['transaction_date'].min()
        to_date = data['transaction_date'].max()

        # create a date range with all the days between the min and max date
        date_range_days = pd.date_range(start=from_date, end=to_date, freq='D')
        #st.write(f"Date range days: {date_range_days}")
        # round the date_rane_days to the beginning of the week
        date_range_weeks = date_range_days.to_period('W').to_timestamp()
        date_range_weeks_unique = date_range_weeks.unique()
        #st.write(f"Date range weeks: {date_range_weeks}")
        #st.write(f"Date range weeks unique: {date_range_weeks_unique}")
        # round the date_rane_days to the beginning of the month
        date_range_months = date_range_days.to_period('M').to_timestamp()
        date_range_months_unique = date_range_months.unique()
        #st.write(f"Date range months: {date_range_months}")
        #st.write(f"Date range months unique: {date_range_months_unique}")
        # round the date_rane_days to the beginning of the quarter
        date_range_quarters = date_range_days.to_period('Q').to_timestamp()
        date_range_quarters_unique = date_range_quarters.unique()
        #st.write(f"Date range quarters: {date_range_quarters}")
        #st.write(f"Date range quarters unique: {date_range_quarters_unique}")
        # round the date_rane_days to the beginning of the year
        date_range_years = date_range_days.to_period('Y').to_timestamp()
        date_range_years_unique = date_range_years.unique()
        #st.write(f"Date range years: {date_range_years}")
        #st.write(f"Date range years unique: {date_range_years_unique}")

        if aggregation_level == 'day':
            date_range = date_range_days
        if aggregation_level == 'week':
            date_range = date_range_weeks_unique
        if aggregation_level == 'month':
            date_range = date_range_months_unique
        if aggregation_level == 'quarter':
            date_range = date_range_quarters_unique
        if aggregation_level == 'year':
            date_range = date_range_years_unique

        # create a dataframe with all the combinations of date_ranges
        date_range_df_base = pd.DataFrame(date_range, columns=['period'])
        date_range = pd.merge(date_range_df_base, date_range_df_base, how='cross', suffixes=('_start', ''))
        date_range = date_range[date_range['period_start'] <= date_range['period']]
        # convert it to date
        date_range['period_start'] = pd.to_datetime(date_range['period_start']).dt.date
        date_range['period'] = pd.to_datetime(date_range['period']).dt.date
        # order by period_start and period_end
        date_range = date_range.sort_values(by=['period_start', 'period'])
        # create a new column with the period number by period_start
        date_range['period_number'] = date_range.groupby('period_start').cumcount()


        # calcaulte first transaction date for each user
        first_transaction_date = data.groupby(['user_id']).agg(
            first_transaction = (aggregation_level_column, 'min')
        ).reset_index()

        # calculate the number of transactions for each user by aggregation level
        transactions_per_user = data.groupby(['user_id', aggregation_level_column]).agg(
            transaction_count = ('invoice_id', 'count'),
            sales = ('sales_value', 'sum')
        ).reset_index()
        # rename aggregation level column to transaction_period
        transactions_per_user = transactions_per_user.rename(columns={aggregation_level_column: 'transaction_period'})

        # create user summary_base dataframe
        user_summary_base = pd.merge(first_transaction_date, transactions_per_user, on='user_id', how='left')
        user_summary_base['transaction'] = 1

        # create user summary per period
        user_summary_per_period_count = user_summary_base.groupby(['first_transaction', 'transaction_period']).agg(
            user_count = ('user_id', 'nunique'),
            transaction_count = ('transaction_count', 'sum'),
            sales = ('sales', 'sum')
        ).reset_index()

        user_summary_per_period_first_transaction_count = user_summary_per_period_count[user_summary_per_period_count['first_transaction'] == user_summary_per_period_count['transaction_period']]
        # renemae columns
        user_summary_per_period_first_transaction_count = user_summary_per_period_first_transaction_count.rename(
            columns={'user_count': 'user_count_first_transaction',
                     'transaction_count': 'transaction_count_first_transaction',
                     'sales': 'sales_first_transaction'}
        )
        # drop transaction_period column
        user_summary_per_period_first_transaction_count = user_summary_per_period_first_transaction_count.drop(columns=['transaction_period'])

        user_summary_per_total = pd.merge(user_summary_per_period_count, user_summary_per_period_first_transaction_count,
                                          left_on='first_transaction', right_on='first_transaction', how='left')
        user_summary_per_total_combinations = pd.merge(date_range, user_summary_per_total, left_on=['period_start', 'period'], right_on=['first_transaction', 'transaction_period'], how='left')
        

        # calculate ratios
        user_summary_per_total_combinations['user_ratio'] = user_summary_per_total_combinations['user_count'] / user_summary_per_total_combinations['user_count_first_transaction']
        user_summary_per_total_combinations['transaction_ratio'] = user_summary_per_total_combinations['transaction_count'] / user_summary_per_total_combinations['transaction_count_first_transaction']
        user_summary_per_total_combinations['sales_ratio'] = user_summary_per_total_combinations['sales'] / user_summary_per_total_combinations['sales_first_transaction']

        # st.dataframe(user_summary_per_total_combinations, use_container_width=True, hide_index=True)

        def diagonal_fill(data):
            '''
            Fill only the top-left of the diagonal with zeros if NaN
            '''
            data_new = data.copy()
            # Fill NaNs with zeros in the top-left of the diagonal
            r_aux = 0
            data_rows_len = len(data_new)
            
            for c in range(1, len(data_new.columns)):
                r_check = data_rows_len - r_aux
                for r in range(r_check):
                    if pd.isna(data_new.iloc[r, c]):
                        data_new.iloc[r, c] = 0.0
                r_aux += 1
            
            return data_new
            
        # users triangles
        users_triangles_count_long = user_summary_per_total_combinations[['period_start', 'period_number', 'user_count']]
        users_triangles_count_wide = users_triangles_count_long.pivot(index='period_start', columns='period_number', values='user_count').reset_index()
        users_triangles_count_wide = diagonal_fill(users_triangles_count_wide)

        users_triangles_percentage_long = user_summary_per_total_combinations[['period_start', 'period_number', 'user_ratio']]
        users_triangles_percentage_wide = users_triangles_percentage_long.pivot(index='period_start', columns='period_number', values='user_ratio').reset_index()
        users_triangles_percentage_wide = diagonal_fill(users_triangles_percentage_wide)

        # transactions triangles
        transactions_triangles_count_long = user_summary_per_total_combinations[['period_start', 'period_number', 'transaction_count']]
        transactions_triangles_count_wide = transactions_triangles_count_long.pivot(index='period_start', columns='period_number', values='transaction_count').reset_index()
        transactions_triangles_count_wide = diagonal_fill(transactions_triangles_count_wide)

        transactions_triangles_percentage_long = user_summary_per_total_combinations[['period_start', 'period_number', 'transaction_ratio']]
        transactions_triangles_percentage_wide = transactions_triangles_percentage_long.pivot(index='period_start', columns='period_number', values='transaction_ratio').reset_index()
        transactions_triangles_percentage_wide = diagonal_fill(transactions_triangles_percentage_wide)

        # sales triangles
        sales_triangles_count_long = user_summary_per_total_combinations[['period_start', 'period_number', 'sales']]
        sales_triangles_count_wide = sales_triangles_count_long.pivot(index='period_start', columns='period_number', values='sales').reset_index()
        sales_triangles_count_wide = diagonal_fill(sales_triangles_count_wide)

        sales_triangles_percentage_long = user_summary_per_total_combinations[['period_start', 'period_number', 'sales_ratio']]
        sales_triangles_percentage_wide = sales_triangles_percentage_long.pivot(index='period_start', columns='period_number', values='sales_ratio').reset_index()
        sales_triangles_percentage_wide = diagonal_fill(sales_triangles_percentage_wide)

    return user_summary_base, user_summary_per_total, users_triangles_count_wide, users_triangles_percentage_wide, transactions_triangles_count_wide, transactions_triangles_percentage_wide, sales_triangles_count_wide, sales_triangles_percentage_wide

def plot_triangles_heatmap(data, type = 'normal', error = False):
    '''
    Plot a heatmap of the sales triangles
    type: 'normal' or 'percentage' or 'integer'
    '''
    data_copy = data.copy()
    text_data = data_copy.iloc[:, 1:]
    values_data = data_copy.iloc[:, 1:]

    if error == True:
        if 'percent':
            data_copy = data_copy.fillna(-0.01)
            text_data = text_data.fillna(-0.01)
            values_data = values_data.fillna(-0.01)

        else:
            data_copy = data_copy.fillna(-1)
            text_data = text_data.fillna(-1)
            values_data = values_data.fillna(-1)
        a = 1

    if type == 'normal':
        texttemplate = "%{text}"
        textfont_size = 10
    
    if type == 'percentage':
        text_data = text_data * 100
        text_data = text_data.round(0)
        # convert it to float
        text_data = text_data.astype(float)
        #data.iloc[:, 1:] = data.iloc[:, 1:].astype(int)
        # textemplate for plotly add the % sign where it is non NA
        texttemplate = "%{text}%"
        textfont_size = 8

    if type == 'integer':
        # convert nan to 0
        text_data = text_data.fillna(-1)
        text_data = text_data.round(0)
        # convert it to integer
        text_data = text_data.astype(int)

        values_data = values_data.fillna(-1)
        values_data = values_data.round(0)
        # convert it to integer
        values_data = values_data.astype(int)
        
        texttemplate = "%{text}"
        textfont_size = 10
    

    x_unique = data_copy.columns[1:]
    # subsctract 1 from each element
    # convert x_unique to string and create a list
    x_unique = x_unique.astype(str).tolist()

    y_unique = data_copy['period_start'].unique()
    # convert y_unique to a string and create a lost
    y_unique = y_unique.astype(str).tolist()

    # st.markdown("We are plotting this data")
    # st.dataframe(data_copy, use_container_width=True, hide_index=True)

    colorscale_to_use = [
        [0, "rgb(255, 255, 255)"],
        [0.01, "rgb(245, 230, 100)"],
        [0.05, "rgb(245, 234, 110)"],
        [0.1, "rgb(40, 191, 63)"],
        [1.0, "rgb(12, 71, 28)"]
    ]
    
    fig = go.Figure(data=go.Heatmap(
            z=values_data,
            x=x_unique,
            y=y_unique,
            hoverongaps=True,
            colorscale=colorscale_to_use,
            # show text on graph
            text=text_data,
            texttemplate=texttemplate,
            textfont={"size": textfont_size}
    ))

    fig.update_yaxes(title_text='Period Start')
    fig.update_xaxes(title_text='Period Number')
    # show all values on x axis

    fig.update_xaxes(tickmode='array', tickvals=x_unique, ticktext=x_unique)
    # show text on graph

    # show all values on y axis
    fig.update_yaxes(tickmode='array',
                     tickvals=y_unique,
                     ticktext=y_unique, autorange="reversed")
    
    # delete the space of the tile and subtitle of the plot
    fig.update_layout(margin=dict(t=25, b=45))
    
    # set height
    fig.update_layout(height=800)
    return fig

st.markdown("#### Options")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    # lookback period in days number input
    lookback_days_default = int(us_cf['lookback_days_default'])
    lookback_period = st.number_input("Lookback period in days", min_value=1, value=lookback_days_default, key='lookback_period_option')
    
with col2:
    # create multiselect for segment
    get_segment_default_values(st.session_state.transaction_maped_dataset, get_session_id())
    st.selectbox("Segment", st.session_state.segment_default_values, key='segment_option')
    # filter the data by segment
    if st.session_state.segment_option != 'All':
        st.session_state.transaction_maped_dataset_filtered = st.session_state.transaction_maped_dataset[st.session_state.transaction_maped_dataset['segment'] == st.session_state.segment_option]
    else:
        st.session_state.transaction_maped_dataset_filtered = st.session_state.transaction_maped_dataset


if 'cummulative_users' not in st.session_state:
    st.session_state.cummulative_users = cummulative_users_calculation(st.session_state.transaction_maped_dataset_filtered, lookback = st.session_state.lookback_period_option)
    st.session_state.user_types = calculating_user_types(st.session_state.transaction_maped_dataset_filtered,
                                                         lookback_periods = [us_cf['lookback_days_1_default'], us_cf['lookback_days_2_default']],
                                                         churning_period = us_cf['churning_days_default'])
    st.session_state.user_sales_triangles_base, st.session_state.user_sales_triangles_calculated, st.session_state.users_triangles_count_wide, st.session_state.users_triangles_percentage_wide, st.session_state.transactions_triangles_count_wide, st.session_state.transactions_triangles_percentage_wide, st.session_state.sales_triangles_count_wide, st.session_state.sales_triangles_percentage_wide = sales_triangles_calculation(
        st.session_state.transaction_maped_dataset_filtered, aggregation_level = us_cf['triangles_aggregation_default'])

# create a button that recalculates the cummulative users if pressed
if st.button("Recalculate users"):
    st.session_state.cummulative_users = cummulative_users_calculation(st.session_state.transaction_maped_dataset_filtered, lookback = st.session_state.lookback_period_option)
    st.session_state.user_types = calculating_user_types(st.session_state.transaction_maped_dataset_filtered,
                                                         lookback_periods = [us_cf['lookback_days_1_default'], us_cf['lookback_days_2_default']],
                                                         churning_period = us_cf['churning_days_default'])
    st.session_state.user_sales_triangles_base,  st.session_state.user_sales_triangles_calculated, st.session_state.users_triangles_count_wide, st.session_state.users_triangles_percentage_wide, st.session_state.transactions_triangles_count_wide, st.session_state.transactions_triangles_percentage_wide, st.session_state.sales_triangles_count_wide, st.session_state.sales_triangles_percentage_wide = sales_triangles_calculation(
        st.session_state.transaction_maped_dataset_filtered, aggregation_level = us_cf['triangles_aggregation_default'])

# if developer mode: show the cummulative users dataframe
if us_cf['developer_mode']:
    st.markdown("## Cummulative Users")
    st.dataframe(st.session_state.cummulative_users, use_container_width=True, hide_index=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("## Total Users - Cummulatice to Date")
    st.checkbox("Show cummulative users data", key='show_cummulative_users_data', value=us_cf['show_cummulative_users_default'])
    fig_cummulative = px.line(st.session_state.cummulative_users, x='date', y='users_to_date')
    st.plotly_chart(fig_cummulative, use_container_width=True, theme=None)
    # if checkbox is checked, show the data
    if st.session_state.show_cummulative_users_data:
        st.dataframe(st.session_state.cummulative_users, use_container_width=True, hide_index=True)

with col2:
    st.markdown(f"## Total Users - Only from {st.session_state.lookback_period_option} days ago to date")
    st.checkbox("Show lookback users data", key='show_lookback_users_data', value=us_cf['show_lookback_users_default'])
    fig_lookback = px.line(st.session_state.cummulative_users, x='date', y='users_lookback')
    st.plotly_chart(fig_lookback, use_container_width=True, theme=None)
    # if checkbox is checked, show the data
    if st.session_state.show_lookback_users_data:
        st.dataframe(st.session_state.cummulative_users, use_container_width=True, hide_index=True)

col1, col2 = st.columns([1, 1])
st.markdown("## User Types")
st.checkbox("Show user types data", key='show_user_types_data', value=us_cf['show_user_types_default'])

def plot_user_types(data):
    fig_line = px.line(data, x='date', y=['new_users', 'returning_users', 'rare_users', 'potentially_churning_users'])
    # put the legend to the buttom of the plot
    fig_line.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    # rename y axis
    fig_line.update_yaxes(title_text='Number of Users')

    fig_bar1 = px.bar(data, x='date', y=['new_users', 'returning_users', 'rare_users', 'potentially_churning_users'])
    fig_bar1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_bar1.update_yaxes(title_text='Number of Users')

    fig_bar2 = px.bar(data, x='date', y=['new_users', 'returning_users', 'rare_users', 'potentially_churning_users'])
    fig_bar2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_bar2.update_yaxes(title_text='Number of Users')

    fig_churn_rate = px.line(data, x='date', y=['new_users_churn_rate', 'returning_users_churn_rate', 'rare_users_churn_rate', 'potentially_churning_users_churn_rate'])
    # put the legend to the buttom of the plot
    fig_churn_rate.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    # rename y axis
    fig_churn_rate.update_yaxes(title_text='Churn Rate')

    return fig_line, fig_bar1, fig_bar2, fig_churn_rate

fig_user_types_line, fig_user_types_bar1, fig_user_types_bar2, fig_user_type_churn_rate= plot_user_types(st.session_state.user_types)
st.plotly_chart(fig_user_types_line, use_container_width=True, theme=None)
st.plotly_chart(fig_user_types_bar1, use_container_width=True, theme=None)
#st.plotly_chart(fig_user_types_bar2, use_container_width=True, theme=None)
st.plotly_chart(fig_user_type_churn_rate, use_container_width=True, theme=None)

# create a table with markdown with explanations of the user types

period_before_days_description = us_cf['lookback_days_2_default']
period_1_days_description = us_cf['lookback_days_1_default']
period_2_days_description = us_cf['lookback_days_2_default']
churning_period_days_description = us_cf['churning_days_default']

new_user_desctiption = f'User who purchesed only in the latest period.'
returning_user_description = f'User who purchesed in two consecutive periods.'
rare_user_description = f'User who purchesed only in the latest period and not in the previous period, but purchased before too. (not a new user)'
potentially_churning_user_description = f'User who purchased in the previous period, but not in the latest period.'

st.markdown(f"""
| User Type|Description| Before Period: (more than {period_before_days_description} ago)|Previous period: ({period_2_days_description} - {period_1_days_description} ago) |Latest period: ({period_1_days_description} ago to given day) |Churning Period: ({churning_period_days_description} day to the future) |
|----------|:-------------|:------:|:----------:|:----------:|:----------:|
| **new user** | {new_user_desctiption} |no|no|yes|no|
| **returning user** | {returning_user_description} |NA|yes|yes|no|
| **rare user** | {rare_user_description} |no|no|yes|no|
| **potentially churning user** | {potentially_churning_user_description} |NA|yes|no|yes|
""")

if st.session_state.show_user_types_data:
    st.dataframe(st.session_state.user_types, use_container_width=True, hide_index=True)

st.markdown("## Sales Triangles")
st.markdown("The sales triangles show the number of transactions for each user in a given period.")

# if developer mode:
if us_cf['developer_mode']:
    st.markdown("### Base Data")
    st.dataframe(st.session_state.user_sales_triangles_base, use_container_width=True, hide_index=True)

    st.markdown("### Calculated Data")
    st.dataframe(st.session_state.user_sales_triangles_calculated, use_container_width=True, hide_index=True)

st.markdown("### Users")
if show_sales_triangles_data:
    st.markdown("#### User Count - Data")
    st.dataframe(st.session_state.users_triangles_count_wide, use_container_width=True, hide_index=True)
if show_sales_triangels_graph:
    st.markdown("#### User Count - Heatmap")
    fig_heatmap = plot_triangles_heatmap(st.session_state.users_triangles_count_wide)
    st.plotly_chart(fig_heatmap, use_container_width=True, theme=None, height=800)
if show_sales_triangles_data:
    st.markdown("#### User Count (%) - Data")
    st.dataframe(st.session_state.users_triangles_percentage_wide, use_container_width=True, hide_index=True)
if show_sales_triangels_graph:
    st.markdown("#### User Count (%) - Heatmap")
    fig_heatmap_percentage = plot_triangles_heatmap(st.session_state.users_triangles_percentage_wide, type='percentage')
    st.plotly_chart(fig_heatmap_percentage, use_container_width=True, theme=None, height=800)

st.markdown("### Transactions")
if show_sales_triangles_data:
    st.markdown("#### Transaction Count - Data")
    st.dataframe(st.session_state.transactions_triangles_count_wide, use_container_width=True, hide_index=True)
if show_sales_triangels_graph:
    st.markdown("#### Transaction Count - Heatmap")
    fig_heatmap = plot_triangles_heatmap(st.session_state.transactions_triangles_count_wide)
    st.plotly_chart(fig_heatmap, use_container_width=True, theme=None, height=800)

if show_sales_triangles_data:
    st.markdown("#### Transaction Count (%) - Data")
    st.dataframe(st.session_state.transactions_triangles_percentage_wide, use_container_width=True, hide_index=True)
if show_sales_triangels_graph:
    st.markdown("#### Transaction Count (%) - Heatmap")
    fig_heatmap_percentage = plot_triangles_heatmap(st.session_state.transactions_triangles_percentage_wide, type='percentage')
    st.plotly_chart(fig_heatmap_percentage, use_container_width=True, theme=None, height=800)

st.markdown("### Sales Value")
if show_sales_triangles_data:
    st.markdown("#### Sales Value - Data")
    st.dataframe(st.session_state.sales_triangles_count_wide, use_container_width=True, hide_index=True)
if show_sales_triangels_graph:
    st.markdown("#### Sales Value - Heatmap")
    fig_heatmap_sales_count = plot_triangles_heatmap(st.session_state.sales_triangles_count_wide, type='integer')
    st.plotly_chart(fig_heatmap_sales_count, use_container_width=True, theme=None, height=800)

if show_sales_triangles_data:
    st.markdown("#### Sales Value (%) - Data")
    st.dataframe(st.session_state.sales_triangles_percentage_wide, use_container_width=True, hide_index=True)
if show_sales_triangels_graph:
    st.markdown("#### Sales Value (%) - Heatmap")
    fig_heatmap_sales_percentage = plot_triangles_heatmap(st.session_state.sales_triangles_percentage_wide, type='percentage', error=True)
    st.plotly_chart(fig_heatmap_sales_percentage, use_container_width=True, theme=None, height=800)

sidebar_empty_space.markdown(" ")
