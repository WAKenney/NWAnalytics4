import streamlit as st
import pandas as pd

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

    # #read the species table from the current directory which should be Github repo
    # speciesFile = currentDir + 'NWspecies220522.xlsx' 

    # speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

    # # Standardize column names to lower case and hyphenated (no spaces).
    # df=df.rename(columns = {'Tree Name':'tree_name','Description':'description','Longitude':'longitude',
    #                             'Latitude':'latitude','Date':'date','Block ID':'block','Tree Number':'tree_number',
    #                             'Species':'species','Genus':'genus','Family':'family','Street':'street',
    #                             'Address':'address','Location Code':'location_code','Ownership Code':'ownership_code',
    #                             'Crown Width':'crown_width','Number of Stems':'number_of_stems','DBH':'dbh',
    #                             'Hard Surface':'hard_surface','Ht to Crown Base':'height_to_crown_base',
    #                             'Total Height':'total_height','Reduced Crown':'reduced_crown','Unbalanced Crown':'unbalanced_crown',
    #                             'Defoliation':'defoliation','Weak or Yellowing Foliage':'weak_or_yellow_foliage',
    #                             'Dead or Broken Branch':'dead_or_broken_branch','Lean':'lean','Poor Branch Attachment':'poor_branch_attachment',
    #                             'Branch Scars':'branch_scars','Trunk Scars':'trunk_scars','Conks':'conks','Rot or Cavity - Branch':'branch_rot_or_cavity',
    #                             'Rot or Cavity - Trunk':'trunk_rot_or_cavity','Confined Space':'confined_space',
    #                             'Crack':'crack','Girdling Roots':'girdling_roots', 'Exposed Roots': 'exposed_roots', 'Recent Trenching':'recent_trenching',
    #                             'Cable or Brace':'cable_or_brace','Conflict with Wires':'wire_conflict',
    #                             'Conflict with Sidewalk':'sidewalk_conflict','Conflict with Structure':'structure_conflict',
    #                             'Conflict with Another Tree':'tree_conflict','Conflict with Traffic Sign':'sign_conflict',
    #                             'Comments':'comments', 'Total Demerits':'demerits','Simple Rating':'simple_rating',
    #                             'Crown Projection Area (CPA)':'cpa', 'Relative DBH':'rdbh','Relative DBH Class':'rdbh_class', 
    #                             'Invasivity':'invasivity', 'Diversity Level':'diversity_level',
    #                             'DBH Class':'dbh_class','Native':'native','Species Suitability':'suitability','Structural Defect':'structural', 
    #                             'Health Defect':'health'})

   
if fileName is not None:

    with st.spinner(text = 'Setting up your data, please wait...'):

        df = getData(fileName)[0]


        
        # display the selected data (select_df) using AgGrid
        select_df = getData(fileName)

        # st.dataframe(select_df)
        
st.dataframe(select_df)