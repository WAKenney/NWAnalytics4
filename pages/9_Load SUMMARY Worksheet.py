import streamlit as st
import pandas as pd
import geopandas as gpd

st.title('Load the SUMMARY data')

info_screen = st.empty()

currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"

fileName ='empty'

df = pd.DataFrame()

fileName = st.file_uploader("Browse for or drag and drop the name of your Neighbourwoods SUMMAY file here", 
    type = ['xlsm', 'xlsx'], 
    key ='fileNameKey')

@st.cache_data(show_spinner=False)
def getData(fileName):
    """Import tree data and species table and do some data organization"""

    if fileName is not None:
        df = pd.read_excel(fileName, sheet_name = "summary", header = 0)

    #read the species table from the current directory which should be Github repo
    speciesFile = currentDir + 'NWspecies220522.xlsx' 

    speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

    # Standardize column names to lower case and hyphenated (no spaces).
    df=df.rename(columns = {'Tree Name':'tree_name','Description':'description','Longitude':'longitude',
                                'Latitude':'latitude','Date':'date','Block ID':'block','Tree Number':'tree_number',
                                'Species':'species','Genus':'genus','Family':'family','Street':'street',
                                'Address':'address','Location Code':'location_code','Ownership Code':'ownership_code',
                                'Crown Width':'crown_width','Number of Stems':'number_of_stems','DBH':'dbh',
                                'Hard Surface':'hard_surface','Ht to Crown Base':'height_to_crown_base',
                                'Total Height':'total_height','Reduced Crown':'reduced_crown','Unbalanced Crown':'unbalanced_crown',
                                'Defoliation':'defoliation','Weak or Yellowing Foliage':'weak_or_yellow_foliage',
                                'Dead or Broken Branch':'dead_or_broken_branch','Lean':'lean','Poor Branch Attachment':'poor_branch_attachment',
                                'Branch Scars':'branch_scars','Trunk Scars':'trunk_scars','Conks':'conks','Rot or Cavity - Branch':'branch_rot_or_cavity',
                                'Rot or Cavity - Trunk':'trunk_rot_or_cavity','Confined Space':'confined_space',
                                'Crack':'crack','Girdling Roots':'girdling_roots', 'Exposed Roots': 'exposed_roots', 'Recent Trenching':'recent_trenching',
                                'Cable or Brace':'cable_or_brace','Conflict with Wires':'wire_conflict',
                                'Conflict with Sidewalk':'sidewalk_conflict','Conflict with Structure':'structure_conflict',
                                'Conflict with Another Tree':'tree_conflict','Conflict with Traffic Sign':'sign_conflict',
                                'Comments':'comments', 'Total Demerits':'demerits','Simple Rating':'simple_rating',
                                'Crown Projection Area (CPA)':'cpa', 'Relative DBH':'rdbh','Relative DBH Class':'rdbh_class', 
                                'Invasivity':'invasivity', 'Diversity Level':'diversity_level',
                                'DBH Class':'dbh_class','Native':'native','Species Suitability':'suitability','Structural Defect':'structural', 
                                'Health Defect':'health'})

   
if fileName is not None:

    with st.spinner(text = 'Setting up your data, please wait...'):

        df = getData(fileName)[0]
        speciesTable = getData(fileName)[1]
        colorsTable = getData(fileName)[2]
        colorsDict = colorsTable.to_dict('dict')['color']

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
        
        # display the selected data (select_df) using AgGrid
        select_df = getData(fileName)

        # st.dataframe(select_df)
        

        
#########################

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
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

# filtdf = filter_dataframe(select_df)

# st.subheader('Filtered Data')

st.dataframe(select_df)