import streamlit as st
import pandas as pd

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Create or Refresh a Neighbourwoods Summary File')

st.markdown("___")

df_trees = st.session_state['df_trees']

df_trees.rename(columns = {'Tree Name' : 'tree_name', 'Date' : 'date', 'Block ID' : 'block', 'Block Id':'block',
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
                            'Address' : 'address', 'DBH Class' : 'dbh_class', 'Relative DBH' : 'rdbh', 'Relative Dbh' : 'rdbh', 
                            'Relative DBH Class' : 'rdbh_class', 'Structural Defects' : 'structural', 
                            'Health Defects' : 'health', 'Description' : 'description', 'Defects' : 'defects', 
                            'Defect Colour' : 'defectColour',  'Total Demerits' : 'demerits', 'Simple Rating' : 'simple_rating'},
                            inplace = True)


def check_data(df):
    '''Checks df_trees for anomolies and adds a column showing errors that may crash the program
    and a column with warnings that may impact the results'''

    with st.spinner(text = 'Checking your data, please wait...'):

        # Older versions of the data didn't include surface roots.  To avoid crashing the app, this function checks to see if surface roots are in the data.
        # If not, then this attribute is removed from the list of column names (cols)

        if df['exposed_roots'].isnull().all():

            cols = ['tree_name','latitude', 'longitude', 'block', 'species', 'street_name', 'address', 'location_code', 'ownership_code', 'number_of_stems', 'dbh',
            'hard_surface', 'crown_width', 'height_to_crown_base', 'total_height', 'reduced_crown', 'unbalanced_crown', 'defoliation',
            'weak_or_yellow_foliage', 'dead_or_broken_branch', 'lean', 'poor_branch_attachment', 'branch_scars', 'trunk_scars', 'conks',
            'branch_rot_or_cavity', 'trunk_rot_or_cavity', 'confined_space','crack', 'girdling_roots', 'recent_trenching', 'cable_or_brace',
            'wire_conflict', 'sidewalk_conflict', 'structure_conflict', 'tree_conflict', 'sign_conflict']

            st.write('It appears that you did not record exposed roots for any entries.  This attribute will be ignored in the "check data" function.')

        else:
            cols = ['tree_name','latitude', 'longitude', 'block', 'species', 'street_name', 'address', 'location_code', 'ownership_code', 'number_of_stems', 'dbh',
            'hard_surface', 'crown_width', 'height_to_crown_base', 'total_height', 'reduced_crown', 'unbalanced_crown', 'defoliation',
            'weak_or_yellow_foliage', 'dead_or_broken_branch', 'lean', 'poor_branch_attachment', 'branch_scars', 'trunk_scars', 'conks',
            'branch_rot_or_cavity', 'trunk_rot_or_cavity', 'confined_space','crack', 'girdling_roots', 'exposed_roots', 'recent_trenching', 'cable_or_brace',
            'wire_conflict', 'sidewalk_conflict', 'structure_conflict', 'tree_conflict', 'sign_conflict']

        

        # Conks is the only attibute with values of 0 or 1 so a species list of column names EXCLUDING conks is set up called 'conditionColsNoConks'

        conditionColsNoConks = ['reduced_crown', 'unbalanced_crown', 'defoliation', 'weak_or_yellow_foliage', 'dead_or_broken_branch', 'lean',
                    'poor_branch_attachment', 'branch_scars', 'trunk_scars', 'branch_rot_or_cavity', 'trunk_rot_or_cavity', 'confined_space',
                    'crack', 'girdling_roots', 'exposed_roots', 'recent_trenching']

        nonTrees = ['dead tree', 'forest', 'hedge','plantable spot', 'snag', 'stump']

        trees = df['tree_name']
       
       #don't need these columnns since they are derived values
        # df.drop(['genus', 'family','cpa', 'rdbh', 'rdbh_class', 'dbh_class', 'health','structural', 'defects', 'defectColour', 'diversity_level', 'invasivity',
        #     'comments', 'suitability', 'description'], 
        #     axis=1, inplace=True)   
      
        # df.drop(['genus', 'family','cpa', 'rdbh', 'rdbh_class', 'dbh_class', 'native', 'color', 'health','structural', 'defects', 'defectColour', 'diversity_level', 'invasivity',
        #     'comments', 'suitability', 'seRegion', 'description', 'geometry'], 
        #     axis=1, inplace=True) 
        


        # Demerits and simple_rating are columns in the legacy format of Neighbourwoods MS 2.6.  If they are present they will be dropped
        if "demerits" in df.columns:
            df.drop(['demerits'])
        if "simple_rating" in df.columns:
            df.drop(['simple_rating'])

        # Make the index tree_name so the df.at function can be used later on
        df.set_index('tree_name', drop = False,  inplace = True) 

        # add a column to df called error and fill all with ok.  The ok is replaced by error message later on
        df['error'] = 'ok' 

        # add a column to df called warning and fill all with ok.  The ok is replaced by warning message later on
        df['warning'] = 'ok'

        # Check if there is a missing value in all columns except for dead, plantable spots etc.  Message is added to the column warnng in df
        
        # Check for duplicate tree names.  If so print a warning
        dupTest = df['tree_name'].duplicated(keep = 'first')
        dup = dupTest[dupTest].index

        if dupTest.values.sum() >= 1:

            st.error('''Uh Oh!  The following tree(s) have duplicate names.  Exit this app, 
            correct any errors in your data input file then re-start this app, re-load the corrected file and proceed.''')
            
            st.write(dup)

        else:
            
            for tree in trees:

                sppName = df.at[tree, 'species']

                if  df.at[tree, 'species'] not in nonTrees:

                    for col in cols:
                        
                        wMessage = df.at[tree, 'warning']

                        if pd.isna(df.at[tree, col]):

                            if df.at[tree, 'warning'] == 'ok':

                                df.at[tree, 'warning'] = 'missing ' + col

                            else:
                                
                                df.at[tree, 'warning'] = wMessage + '; missing ' + col


        # Check for invalide codes in the tree condition columns.  Must be either 0, 1, 2, or 3.  Using tree names of entries exclusing nontrees like dead, forest, hedge, etc.
        
        for col in conditionColsNoConks:
                
            wMessage = df.at[tree, 'error']

            if df.at[tree, col] not in [0, 1, 2, 3]:

                if df.at[tree, 'error'] == 'ok':

                    df.at[tree, 'error'] = 'invalide code in ' + col

                else:
                    
                    df.at[tree, 'error'] = wMessage + '; invalide code in ' + col

                    
        #check for invalide codes for conks.  This is done separately because conks only have codes of 0 or 1            
        wMessage = df.at[tree, 'error']

        if df.at[tree, 'conks'] not in [0, 1]:

            if df.at[tree, 'error'] == 'ok':

                df.at[tree, 'error'] = 'Invalide code in conks'

            else:
                
                df.at[tree, 'error'] = wMessage + '; invalide code in conks'

        #check for invalide codes for ownership.            
        wMessage = df.at[tree, 'error']

        if df.at[tree, 'ownership_code'] not in ['c', 'p', 'j']:

            if df.at[tree, 'error'] == 'ok':

                df.at[tree, 'error'] = 'Invalide code in ownership'

            else:
                
                df.at[tree, 'error'] = wMessage + '; invalide code in ownership'


        # Record 'invalide species code' in the Error column if species code used is not in the species code column of the speciesTable
        wMessage = df.at[tree, 'error']

        # if df.at[tree, 'species'] not in speciesTable['species'].tolist():
        if pd.isnull(df.at[tree, 'species']):

            if df.at[tree, 'error'] == 'ok':

                df.at[tree, 'error'] = 'Invalide species code'

            else:
                
                df.at[tree, 'error'] = wMessage + '; invalide species code'

        # Record a warning if identified only to genus     
        wMessage = df.at[tree, 'warning']

        if pd.notna(sppName):

            if 'species' in sppName: # Entries identified only to genus will have the word species in the name like Maple Species.  If this happens, record a warning

                if wMessage == 'ok':

                    df.at[tree, 'warning'] = 'Only genus identified'

                else:
                    
                    df.at[tree, 'warning'] = wMessage + '; only genus identified'

        
        # remove rows in the output table (df) that have ok in both the warning and error columns in otherwords there are no problems
        for tree in trees:
            df = df[(df["warning"].str.contains("ok") & df["error"].str.contains("ok")) == False]
            
        dfCheck = df.copy()

        df.drop(['error', 'warning'], axis=1, inplace=True)

        st.markdown('---')
        st.subheader('Errors and Warnings')
        st.markdown('''The following table shows entries with errors and warnings.  Scroll to the right to view the messages in the final two columns. 
                        Warnings highlight issues that may result in some lost information whereas **errors _may_ result in the app crashing.  You should 
                        correct errors before proceeding.**
                        You can filter the columns just as you would in the main table.
        ''')

        st.dataframe(dfCheck, hide_index=True)

if "df_trees" not in st.session_state:

    st.error("You haven't loaded a file yet.  Either go to the 'Create or Refresh...' function in the side bar or the ' Load and Existing...")


check_data(st.session_state['df_trees'])
