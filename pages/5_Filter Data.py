import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,)

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Create or Refresh a Neighbourwoods Summary File')

st.markdown("___")

with st.expander("Click here for hints on filtering your data", expanded=False):
    st.markdown("""The table below shows your inventory data 
    and can be filtered much as you would a Microsoft Excel worksheet.  Scroll across the columns and place your cursor on the header of the
    column that you wish to filter.  As you do so, an icon of three lines will appear in the header, click on this icon.  The type of filter
    will depend on the type of data in that column.  For text data, you will see a list of all the options in that column with a checkbox to the left of each line.  To filter 
    out specific items first click on the check box beside _Select All_ to switch off all the items.  Now, click on the box(es) beside the items
    you want in your filter.  Note that you can type in an item name to shorten the list.  ***Once you have selected everything you want in the
    filter, you must click on the Update button at the top left of the table***.  Your filtered data will now be used in all the functions you select
    from the sidebar at the left.
    For numerical data you will have the option to filter using comparison types such as equal to, greater than, etc.
    Remember to click on the _Update_ button to commit your filter to the analysis functions. 
    Columns with an active filter will have an icon that looks like a funnel in the header.        
    To clear all filters and return to the full data set, click on the Update button.
    Note: that you can save your filtered data as an Excel workbook by clicking on the link at the bottom of the FILTERED data table.""")


# def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
def filter_dataframe(df):
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    st.download_button("Download filtered data as a csv file",
                       df.to_csv().encode('utf-8'),
                       file_name = "Filtered_data.csv",
                       mime = 'text/csv')


    return df

#Call filter_dataframe to do the filtering and save the result as select_df
select_df = filter_dataframe(st.session_state['df_trees'])

#Store the filtered data (select_df in the session_state as select_df)
if select_df not in st.session_state:

    st.session_state['select_df'] = []

st.session_state['select_df'] = select_df

#Add the number of entries in select_df to session_state
select_tree_count = select_df.shape[0]

if select_df not in st.session_state:

    st.session_state['select_tree_count'] = []

st.session_state['select_tree_count'] = select_tree_count

#show the filtered dataframe select_df and the number of entries

if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:
    st.markdown(f"### There are {st.session_state['select_tree_count']} entries currently loaded. ")
else:
    st.write(f"There are {st.session_state['total_tree_count']} entries currently loaded. ")

# st.write(f"You have {select_tree_count:,} trees of the in your filtered database.")

st.dataframe(select_df)


