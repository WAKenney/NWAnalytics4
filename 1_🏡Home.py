import pandas as pd
import geopandas as gpd
import streamlit as st
from datetime import datetime

st.set_page_config(layout="centered")


currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"

# speciesFile = currentDir + 'NWspecies220522.xlsx'
speciesFile = 'NWspecies220522.xlsx'

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'nw4_splash_page.png'

titleCol2.image(title)



now = datetime.now()
formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")
st.write("Last updated:", formatted_date)



with st.expander("Click here for help in getting started.", expanded=False):
    st.markdown("""
        Neighbourwoods is a community-based program to assist community groups in the stewardship of the urban forest in their neighbourhood.
        Using NWAnalytics, you can map and analyze various aspects of the urban forest that will help you develop and implement stewardship strategies.
        At present, you must first have your Neighbourwoods tree inventory data in a Neighbourwoods MS excel workbook (version 2.6 or greater).

        To get started, select your Neighbourwoods MS excel workbook at the sidebar on the left. Once your data has been uploaded (this may take 
        a few minutes if you have a big file, be patient) you will be asked to select the functions you want to display.  Select as many as you 
        want from the dropdown list __AND CLICK ON CONTINUE__.  The selected analyses will be shown in the main frame.

        You can conduct these analyses on all the data, or you can filter the data for specific queries. For hints on filtering your data, click on the button below.

        In various places you will have opportunities to click on a box 
        for more information, just as you are reading this text.  To close these boxes, simply click on the header button again.

        Click on the following link to read more about Neighbourwoods: http://neighbourwoods.org/')

        For support, contact Andy Kenney at:     a.kenney@utoronto.ca
""")

st.session_state['speciesTable'] = []

st.session_state['colorsTable'] = []

st.session_state['df_trees'] = []

st.session_state['select_df'] = []

st.session_state['select_df'] = []

st.session_state['total_tree_count'] = []

st.session_state['select_tree_count'] = []

st.session_state['avLon'] = []

st.session_state['avLat'] = []


@st.cache_data(show_spinner="Loading the species table, please wait ...")
def getSpeciesTable():
    '''Load the species table from the Neighburwoods repo'''

    speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

    # st.dataframe(speciesTable)

    if "speciesTable" not in st.session_state:

        st.session_state['speciesTable'] = []

    st.session_state['speciesTable'] = speciesTable
    
    return speciesTable


speciesTable = getSpeciesTable()


# get the species specific colour from the species table for each entry and create the coloursTable
colorsTable = pd.read_excel(speciesFile,sheet_name = "colors")

colorsTable.set_index('taxon', inplace = True)

st.session_state['colorsTable'] = colorsTable