import streamlit as st
import pandas as pd
# from streamlit_extras.let_it_rain import rain 


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
            
            st.warning("Uh oh! The file you selected doesn't appear to be a SUMMARY file. You may have to run the 'Create or Refresh Summary Worksheet' function first.")

        
def fix_column_names(df_trees):
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
    

# def set_data_types(df_trees):

#     # df_trees = df_trees.astype({'street_code': 'category', 'reduced_crown': 'category'})
#     df_trees = df_trees.astype({'block' : 'category', 'tree_number' : 'int64', 'house_number' : 'str', 'street_code' : 'category', 'species_code' : 'category', 
#                                    'location_code' : 'category', 'ownership_code' : 'category', 
#                                    'number_of_stems' : 'int64', 'dbh' : 'float64', 'hard_surface' : 'int64', 
#                                    'crown_width' : 'int64', 'height_to_crown_base' : 'int64', 
#                                    'total_height' : 'int64', 'reduced_crown' : 'category', 
#                                    'unbalanced_crown' : 'category', 'defoliation' : 'category', 
#                                    'weak_or_yellow_foliage' : 'category', 'dead_or_broken_branch' : 'category', 'lean' : 'category', 
#                                    'poor_branch_attachment' : 'category', 'branch_scars' : 'category', 
#                                    'trunk_scars' : 'category', 'conks' : 'category', 'branch_rot_or_cavity' : 'category', 
#                                    'trunk_rot_or_cavity' : 'category', 'confined_space' : 'category', 
#                                    'crack' : 'category', 'girdling_roots' : 'category',  'exposed_roots' : 'category', 
#                                    'recent_trenching' : 'category', 'cable_or_brace' : 'category', 
#                                    'wire_conflict' : 'category', 'sidewalk_conflict' : 'category', 
#                                    'structure_conflict' : 'category', 'tree_conflict' : 'category', 
#                                    'sign_conflict' : 'category', 'comments' : 'category',  
#                                    'street' : 'category', 'family' : 'category', 'genus' : 'category', 'species' : 'category', 
#                                    'invasivity' : 'category', 'suitability' : 'category', 
#                                    'diversity_level' : 'category', 'native' : 'category', 'cpa' : 'float64', 
#                                    'address' : 'str', 'dbh_class' : 'category', 'rdbh' : 'float64', 
#                                    'rdbh_class' : 'category', 'structural' : 'category', 
#                                    'health' : 'category', 'description' : 'str', 'defects' : 'category', 
#                                    'defectColour' : 'category', 'demerits' :  'int64', 'simple_rating' : 'category'})

#     return df_trees


# def let_it_rain():
#     rain(emoji="🌳", font_size=40, falling_speed=3, animation_length=0.75)


df_trees = getData(fileName)

if df_trees is not None:

    df_trees = fix_column_names(df_trees)

    # df_trees = set_data_types(df_trees)

    st.write(df_trees.dtypes)

    screen1 = st.empty()
    
    st.dataframe(df_trees)

    #Add df_trees to session_state
    if "df_trees" not in st.session_state:

        st.session_state['df_trees'] = []

    st.session_state['df_trees'] = df_trees

    total_tree_count = df_trees.shape[0]

    #Add select_df to session_state but at this point it is the same as df_trees.  This will be replaced if a filter is applied
    if "select_df" not in st.session_state:

        st.session_state['select_df'] = []

    st.session_state['select_df'] = df_trees
    st.session_state['select_tree_count'] = total_tree_count

    #add average latitude and average longitude to session state
    st.session_state['avLat'] = df_trees['latitude'].mean()
    st.session_state['avLon'] = df_trees['longitude'].mean()
    
    if "total_tree_count" not in st.session_state:

        st.session_state['total_tree_count'] = []

    st.session_state['total_tree_count'] = total_tree_count

    # let_it_rain()

    screen1.markdown(f'#### Your data is loaded with :red[{total_tree_count}] entries. You can now proceed with the mapping and analyses by selecting a function from the sidebar at the left. :arrow_backward:')
