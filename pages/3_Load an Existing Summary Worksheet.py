import streamlit as st
import pandas as pd
from streamlit_extras.let_it_rain import rain

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Load an Existing Neighbourwoods Summary File')

st.markdown("___")

fileName ='empty'

# df = pd.DataFrame()

# fileName = st.file_uploader("Browse for or drag and drop the name of your Neighbourwoods SUMMAY file here", 
#     type = ['xlsm', 'xlsx'], 
#     key ='fileNameKey')

fileName = st.file_uploader("Browse for or drag and drop the name of your Neighbourwoods SUMMAY file here", 
    type = ['xlsm', 'xlsx'])


@st.cache_data(show_spinner=False)
def getData(fileName):

    """Import tree data and species table and do some data organization"""

    if fileName is not None:

        df = pd.DataFrame()

        try:
            df = pd.read_excel(fileName, sheet_name = "trees", header = 0)
 
        except ValueError:

            try:

                df = pd.read_excel(fileName, sheet_name = "summary", header = 0)

            except Exception as e:

                st.error(e)

                # ("Oops, are you sure your file is a Neighbourwoods SUMMARY file with a worksheet called 'summary'?")

        if 'Description' in df.columns:

            return df

        else:
            
            st.warning("Uh oh! The file you selected doesn't appear to be a SUMMARY file. You may have to run the 'Create or Refresh' function first.")

             
        
def fix_column_names(df):
    '''Standardize column names to lower case and hyphenated (no spaces) as well as correct various 
    different spelling of names.'''
    
    return df_trees.rename(columns = {'Tree Name' : 'tree_name', 'Date' : 'date', 'Block ID' : 'block', 'Block Id':'block',
                                   'Tree Number' : 'tree_number', 'House Number' : 'house_number', 'Street Code' : 'street_code', 
                                   'Species Code' : 'species_code', 'Location Code' : 'location_code', 'location':'location_code', 
                                   'Ownership Code' : 'ownership_code','ownership':'ownership_code','Ownership code':'ownership_code', 
                                   'Number of Stems' : 'number_of_stems', 'DBH' : 'dbh', 'Hard Surface' : 'hard_surface', 
                                   'Crown Width' : 'crown_width', 'Ht to Crown Base' : 'height_to_crown_base', 
                                   'Total Height' : 'total_height', 'Reduced Crown' : 'reduced_crown', 
                                   'Unbalanced Crown' : 'unbalanced_crown', 'Defoliation' : 'defoliation', 
                                   'Weak or Yellowing Foliage' : 'weak_or_yellow_foliage', 
                                   'Dead or Broken Branch' : 'dead_or_broken_branch', 'Lean' : 'lean', 
                                   'Poor Branch Attachment' : 'poor_branch_attachment', 'Branch Scars' : 'branch_scars', 
                                   'Trunk Scars' : 'trunk_scars', 'Conks' : 'conks', 'Rot or Cavity - Branch' : 'branch_rot_or_cavity', 
                                   'Rot or Cavity - Trunk' : 'trunk_rot_or_cavity', 'Confined Space' : 'confined_space', 
                                   'Crack' : 'crack', 'Girdling Roots' : 'girdling_roots', 'Exposed Roots' :  'exposed_roots', 
                                   'Recent Trenching' : 'recent_trenching', 'Cable or Brace' : 'cable_or_brace', 
                                   'Conflict with Wires' : 'wire_conflict', 'Conflict with Sidewalk' : 'sidewalk_conflict', 
                                   'Conflict with Structure' : 'structure_conflict', 'Conflict with Another Tree' : 'tree_conflict', 
                                   'Conflict with Traffic Sign' : 'sign_conflict', 'Comments' : 'comments', 
                                   'Longitude' : 'longitude', 'Latitude' : 'latitude', 
                                   'Street' : 'street', 'Family' : 'family', 'Genus' : 'genus', 'Species' : 'species', 
                                   'Invasivity' : 'invasivity', 'Species Suitability' : 'suitability', 
                                   'Diversity Level' : 'diversity_level', 'Native' : 'native', 'Crown Projection Area (CPA)' : 'cpa', 
                                   'Address' : 'address', 'DBH Class' : 'dbh_class', 'Relative DBH' : 'rdbh', 
                                   'Relative DBH Class' : 'rdbh_class', 'Structural Defects' : 'structural', 
                                   'Health Defects' : 'health', 'Description' : 'description', 'Defects' : 'defects', 
                                   'Defect Colour' : 'defectColour',  'Total Demerits' : 'demerits', 'Simple Rating' : 'simple_rating'})




    # return df.rename(columns = {'Tree Name':'tree_name','Description':'description','Longitude':'longitude',
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

def let_it_rain():
    rain(emoji="🌳", font_size=40, falling_speed=3, animation_length=0.75)


df_trees = getData(fileName)

if df_trees is not None:

    df_trees = fix_column_names(df_trees)

    screen1 = st.empty()
    
    st.dataframe(df_trees)

    if df_trees not in st.session_state:

        st.session_state['df_trees'] = []

    st.session_state['df_trees'] = df_trees

    let_it_rain()

    screen1.markdown('### Your data is loaded.  You can now proceed with the mapping and analyses by selecting a function from the sidebar at the left.')

