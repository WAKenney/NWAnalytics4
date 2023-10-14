import streamlit as st
import pandas as pd

st.title('Load the SUMMARY data')

currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/main/"

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

    def defect_setup(df):
        """
        This def adds a column to the dataframe containing text descriptions for the level of defects based on the yes or no 
        respones in the structural and health columns of the input data.
        """

        if ((df['structural'] == 'no') & (df['health'] =='no')):
            return 'No major defects'
        elif ((df['structural'] == 'yes') & (df['health'] =='no')):
            return 'Major structural defect(s)'
        elif ((df['structural'] == 'no') & (df['health'] =='yes')):
            return 'Major health defect(s)'
        elif ((df['structural'] == 'yes') & (df['health'] =='yes')):
            return 'Major structural AND health defect(s)'
        else:
            return 'Condition was not assessed'

    df['defects'] = df.apply(defect_setup, axis = 1) #Apply the defect_setup fucntion to all rows of the trees dataframe
    
    def setDefectColour(df):
        ''' sets a colour name in column defectColour based on the value in column defects.  This is for mapping'''
        
        if df['defects'] == 'No major defects':
            return 'darkgreen'

        elif df['defects'] == 'Major structural defect(s)':
            return 'yellow'
        
        elif df['defects'] == 'Major health defect(s)':
            return 'greenyellow'

        elif df['defects'] == 'Major structural AND health defect(s)':
            return 'red'
        
        else:
            return 'black'

    # Apply defectColour function to all rows of the trees dataframe
    df['defectColour'] = df.apply(setDefectColour, axis = 1) 

    #Read variables from the speices table and add them to the trees table
    # df = pd.merge(df, speciesTable[['species', 'seRegion']], on="species", how="left", sort=False)
    # df = pd.merge(df, speciesTable[['species', 'color']], on="species", how="left", sort=False)
    df = pd.merge(df, speciesTable[['species', 'color', 'seRegion']], on="species", how="left", sort=False)

    #Record a suitability of very poor for any species that is invasive based on the species table
    df.loc[(df.invasivity =='invasive'), 'suitability'] = 'very poor'

    df.merge(speciesTable, how = 'left', on = 'species', sort = False )

    # save the 'data' pandas dataframe as a geodataframe
    df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude)).copy() 
    
    # Save the inventory dates as a string.  Otherwise an error is thrown when mapping
    df['date'] = df['date'].astype(str)

    # get the species specific colour from the species table for each entry and create the coloursTable
    colorsTable = pd.read_excel(speciesFile,sheet_name = "colors")
    colorsTable.set_index('taxon', inplace = True)

    return [df, speciesTable, colorsTable]



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

        st.dataframe(select_df)
        