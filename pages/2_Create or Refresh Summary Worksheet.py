import io
import pandas as pd
import geopandas as gpd
import streamlit as st
import datetime
import pytz
import folium
from streamlit_folium import folium_static
from shapely.geometry import Point


# from io import BytesIO
# import base64


st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"

speciesFile = currentDir + 'NWspecies220522.xlsx'

attributeNames = ['reduced_crown', 'unbalanced_crown', 'defoliation',
    'weak_or_yellow_foliage', 'dead_or_broken_branch',  'lean', 'poor_branch_attachment',	
    'branch_scars', 'trunk_scars', 'conks', 'branch_rot_or_cavity', 
    'trunk_rot_or_cavity', 'confined_space', 'crack', 'exposed_roots', 'girdling_roots', 'recent_trenching']


#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Create or Refresh a Neighbourwoods Summary File')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()

st.markdown("___")


def create_summary_data():
    '''This function adds various values to the inventory input datasheet that are used in the various analyses that follow.  
    This is the MAIN finction for 2_Create or Refresh Summary Worksheet.  The output is df_trees which is saved in the st.session_state for usein other
    apps of this collection.'''

    df_trees = pd.DataFrame()
 
    @st.cache_data(show_spinner="Loading the species table, please wait ...")
    def getSpeciesTable():
        '''Load the species table from the Neighburwoods repo'''

        speciesFile = currentDir + 'NWspecies220522.xlsx'

        speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

        # st.dataframe(speciesTable)


        if "speciesTable" not in st.session_state:

            st.session_state['speciesTable'] = []

        st.session_state['speciesTable'] = speciesTable

        
        return speciesTable


    speciesTable = getSpeciesTable()


    @st.cache_data(show_spinner="Loading your data, please wait ...")
    def get_raw_data(fileName):

        '''This loads the basic inventory data without any of the derived columns'''

        if fileName is not None:

            df_trees = pd.DataFrame()
            # df_streets = pd.DataFrame()

            try:

                df_trees = pd.read_excel(fileName, sheet_name = 'trees', header = 0)
            
            except:
            
                st.error("Ooops something is wrong with your data file!")
            
            return df_trees


    df_trees = get_raw_data(fileName)


    @st.cache_data(show_spinner="Loading your street data, please wait ...")
    def get_streets():

        if fileName is not None:

            df_streets = pd.DataFrame()

            df_streets = pd.read_excel(fileName, sheet_name = 'streets', header = 0)

            df_trees.rename(columns = {'ADDRESS' : 'street_code', 'ADDRESSNAME' : 'street_name',
                                       'Street Code':'street_code','Street Name':'street_name'})
            
            if 'df_streets' not in st.session_state:

                st.session_state['df_streets'] = []

            st.session_state['df_streets'] = df_streets

            return df_streets


    df_streets = get_streets()


    def clean_and_expand_data(df_trees):
       
        df_trees.rename(columns = {'Tree Name' : 'tree_name', 'Date' : 'date', 'Block ID' : 'block', 'Block Id':'block', 'Block':'block',
                                   'Tree Number' : 'tree_number', 'Tree No' : 'tree_number', 'House Number' : 'house_number', 'Street Code' : 'street_code', 
                                   'Species Code' : 'species_code', 'Location Code' : 'location_code', 'location':'location_code', 
                                   'Ownership Code' : 'ownership_code','ownership':'ownership_code','Ownership code':'ownership_code', 
                                   'Number of Stems' : 'number_of_stems', 'DBH' : 'dbh', 'Hard Surface' : 'hard_surface', 'Hard surface' : 'hard_surface',
                                   'Crown Width' : 'crown_width', 'Ht to Crown Base' : 'height_to_crown_base', 
                                   'Total Height' : 'total_height', 'Reduced Crown' : 'reduced_crown', 
                                   'Unbalanced Crown' : 'unbalanced_crown', 'Defoliation' : 'defoliation', 'Weak or Yellow Foliage' : 'weak_or_yellow_foliage',
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
                                   'Address' : 'address', 'DBH Class' : 'dbh_class', 'Relative DBH' : 'rdbh','Relative Dbh' : 'rdbh', 
                                   'Relative DBH Class' : 'rdbh_class', 'Structural Defects' : 'structural', 
                                   'Health Defects' : 'health', 'Description' : 'description', 'Defects' : 'defects', 
                                   'Defect Colour' : 'defectColour',  'Total Demerits' : 'demerits', 'Simple Rating' : 'simple_rating'},
                                   inplace = True)
       

        dataCols =df_trees.columns

        df_streets.rename(columns = {'ADDRESS':'street_code','ADDRESSNAME':'street_name','street':'street_code','street name':'street_name' }, inplace = True)

        if 'xy' in dataCols:
            df_trees[['Latitude', 'Longitude']] = df_trees['xy'].str.split(',', 1, expand=True)
            df_trees.drop('xy', axis=1, inplace=True)

        #check to make sure Lat and Lon aren't mixed up.  If average Latitude is greater than 60 it is LIKELY really longitude so swap the names

        # if avLat > 60:   
        #     df_trees=df_trees.rename(columns = {'Y coordinate':'Latitude','X coordinate':'Longitude'})

        df_trees['species_code'] = df_trees['species_code'].str.lower()
        df_trees['species_code'] = df_trees['species_code'].str.strip()

        df_trees['street_code'] = df_trees['street_code'].str.lower()
        df_trees['street_code'] = df_trees['street_code'].str.strip()

        df_trees['ownership_code'] = df_trees['ownership_code'].str.lower()
        df_trees['ownership_code'] = df_trees['ownership_code'].str.strip()

        df_trees['location_code'] = df_trees['location_code'].str.lower()
        df_trees['location_code'] = df_trees['location_code'].str.strip()

        df_streets['street_code'] = df_streets['street_code'].str.lower()
        df_streets['street_code'] = df_streets['street_code'].str.strip()

        df_streets['street_name'] = df_streets['street_name'].str.strip()

        if 'tree_name' not in dataCols:
            df_trees["tree_name"] = df_trees.apply(lambda x : str(x["block"]) + '-' +  str(x["tree_number"]), axis=1)

        df_trees = df_trees.merge(df_streets.loc[:,['street_code', 'street_name']], how='left')

        if 'exposed_roots' not in df_trees.columns:
            df_trees.insert(30,"exposed_roots",'')

        cols = df_trees.columns





        # def getOrigin():
            
        #     origin = pd.read_excel(speciesFile, sheet_name = 'origin')

        #     return origin


        # df_origin = getOrigin()


        # def getEcodistricts():

        #     gpd_ecodistricts = gpd.read_file(r"https://github.com/WAKenney/NWAnalytics/blob/master/OntarioEcodistricts.gpkg")
              
        #     return gpd_ecodistricts


        # gpd_ecodistricts = getEcodistricts()





        def getCodes():

            codes = pd.read_excel(speciesFile, sheet_name = 'codes')

            return codes

        df_codes = getCodes()

        df_trees = df_trees.merge(speciesTable.loc[:,['species_code','family', 'genus','species', 'Max DBH', 'invasivity',
            'suitability', 'diversity_level']], how='left')

        df_trees=df_trees.rename(columns = {'Max DBH':'max_dbh'})


        def get_ecodistrict():
            '''Determines the name of the ecodistrict that the average latitude and average longitude are in.  This is used
            to determine native vs non-native based on ecodistricts and Little's tree species range maps.'''
                
            currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"
            
            # import the geopackage with the map (geometries) of all Ecodistricts'''
                
            ecodistricts = gpd.read_file(currentDir + "OntarioEcodistricts.gpkg")
            
            #create a point with avLon and avLat from session_state
            avLat = df_trees['latitude'].mean()

            if 'avLat' not in st.session_state:
                avLat = [] 

            st.session_state['avLat'] = avLat
            
            avLon = df_trees['longitude'].mean()

            if 'avLon' not in st.session_state:
                avLon = [] 

            st.session_state['avLon'] = avLon
                        
            point = Point(avLon, avLat)

            #Make the point object a geodataframe
            point_gdf = gpd.GeoDataFrame(geometry=[point])

            #determine which of the ecodistrict polygons the point is in
            selected_polygon = gpd.tools.sjoin(point_gdf, ecodistricts, predicate="within", how='left')

            #read the name of the selected ecodistrict and call it ecodName
            ecodistrict_name = (selected_polygon.ECODISTR_1[0])

            return ecodistrict_name

        activeEcodist = get_ecodistrict()


        def origin(df_trees):
          
            df_origin = pd.read_excel(speciesFile, sheet_name = 'origin')

            df_trees = df_trees.merge(df_origin.loc[:,['species_code', activeEcodist]], how='left')

            df_trees=df_trees.rename(columns = {activeEcodist:'origin'})

            return df_trees


        df_trees = origin(df_trees)

        
        def cpa(cw):

            '''
            calculate crown projection area
            '''

            if pd.isnull(df_trees['crown_width'].iloc[0]):

                cpa = 'n/a'
            else:

                cpa = ((cw/2)**2)*3.14
                # cpa= int(cpa)

            return cpa

        df_trees['Crown Projection Area (CPA)'] = df_trees['crown_width'].apply(lambda x: (cpa(x)))

        df_trees["Address"] = df_trees.apply(lambda x : str(x["house_number"]) + ' ' +  str(x["street_name"]), axis=1)


        def dbhClass(df):

            if df['dbh']<20:

                return 'I'

            elif df['dbh']<40:

                return 'II'

            elif df['dbh']<60:

                return 'III'

            else: 

                return 'IV'

        df_trees['DBH Class'] = df_trees.apply(dbhClass, axis =1)


        def rdbh():

            df_trees['Relative Dbh'] =df_trees.apply(lambda x: 'n/a' if pd.isnull('dbh') else x.dbh/x.max_dbh, axis =1).round(2)

            df_trees.drop('max_dbh', axis=1, inplace=True)


        rdbh()

        df_trees['Relative DBH Class'] = pd.cut(x=df_trees['Relative Dbh'], bins=[0, 0.25, 0.5, 0.75, 3.0], labels = ['I', 'II', 'III','IV'])


        def structural(df):

            if df['unbalanced_crown'] ==3:

                return 'yes' 

            elif df['dead_or_broken_branch'] == 3:

                return 'yes'

            elif df['lean'] == 3:

                return 'yes'

            elif df['dead_or_broken_branch'] == 3:

                return 'yes'

            elif df['poor_branch_attachment'] == 3:

                return 'yes'

            elif df['trunk_rot_or_cavity'] == 3:

                return 'yes'

            elif df['branch_rot_or_cavity'] == 3:

                return 'yes'

            elif df['crack'] == 3:

                return 'yes'

            elif df['cable_or_brace'] == 'y':

                return 'yes'

            else:

                return 'no'


        df_trees['Structural Defects']= df_trees.apply(structural, axis =1)


        def health(df):

            if df['defoliation'] ==3:

                return 'yes' 

            elif df['weak_or_yellow_foliage'] == 3:

                return 'yes'

            elif df['trunk_scars'] == 3:

                return 'yes'

            elif df['conks'] == 3:

                return 'yes'

            elif df['girdling_roots'] == 3:

                return 'yes'

            elif df['recent_trenching'] == 3:

                return 'yes'

            else:

                return 'no'


        df_trees['Health Defects']= df_trees.apply(health, axis =1)


        def desc(df):

            df_cond = pd.DataFrame(columns=attributeNames)

            df['Description'] = []

            df['Description'] = "Tree {} is a {} at {}. The most recent assessment was done on {}.".format(df['tree_name'], df['species'], df['Address'], df['date'])
            # df['Description'] = f"Tree {df['tree_name']} is a {df['species']} at {df['Address']}. The most recent assessment was done on {df['date']:%B %d, %y}."

            if df['Structural Defects'] == 'yes' and df['Health Defects'] =='yes':

                df['Description'] = df['Description'] + ' It has significant structural AND health defects'
            
            elif df['Structural Defects'] == 'yes':

                df['Description'] = df['Description'] + ' It has at least one significant structural defect.'
            
            elif df['Health Defects'] == 'yes':

                df['Description'] = df['Description'] + ' It has at least one significant health defect.'
            
            elif df['Structural Defects'] == 'yes' and df['Health Defects'] =='yes':

                df['Description'] = df['Description'] + ' It has significant structural AND health defects'
            
            else:

                df['Description'] = df['Description'] + ' It has no SIGNIFICANT health or structural defects.'

            df['Description'] = df['Description'] + " It has a DBH of {} cm, a total height of {:,.0f} m and a crown width of {:,.0f}m.".format(df['dbh'], df['total_height'], df['crown_width'])

            if pd.notnull(df['hard_surface']):

                df['Description'] = df['Description'] + " The area under the crown is {:,.0f}% hard surface. ".format(df['hard_surface'])

            return df


        df_trees = df_trees.apply(desc, axis =1)


        def condition():
            '''This creates a series called code_names holding the column 
            names from df_codes and an empty df called df_cond 
            which is then filled with the text from df_codes 
            corresponding to each of the scores from df_trees for each column 
            in code_names. The result is additon of condition descriptions to
            df_trees['Description']'''

            df_cond = pd.DataFrame(columns=attributeNames)
            
            for column in attributeNames:

                df_cond[column]=df_trees[column].map(df_codes[column]).fillna('')
                
            condition = df_cond.apply(lambda row: ''.join(map(str, row)), axis=1)

            df_trees['Description'] = df_trees['Description'] + condition


        condition() # This calls the function condition()


        def defect_setup(df):
            """
            This def adds a column to the dataframe containing text descriptions for the level of defects based on the yes or no 
            respones in the structural and health columns of the input data.
            """

            if ((df['Structural Defects'] == 'no') & (df['Health Defects'] =='no')):

                return 'No major defects'

            elif ((df['Structural Defects'] == 'yes') & (df['Health Defects'] =='no')):

                return 'Major structural defect(s)'

            elif ((df['Structural Defects'] == 'no') & (df['Health Defects'] =='yes')):

                return 'Major health defect(s)'

            elif ((df['Structural Defects'] == 'yes') & (df['Health Defects'] =='yes')):

                return 'Major structural AND health defect(s)'

            else:

                return 'Condition was not assessed'


        df_trees['defects'] = df_trees.apply(defect_setup, axis = 1) #Apply the defect_setup fucntion to all rows of the trees dataframe
            
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
        df_trees['defectColour'] = df_trees.apply(setDefectColour, axis = 1) 

        #Read variables from the speices table and add them to the trees table
        df_trees.merge(speciesTable[['species', 'color', 'seRegion']], on="species", how="left", sort=False)

        #Record a suitability of very poor for any species that is invasive based on the species table
        df_trees.loc[(df_trees.invasivity =='invasive'), 'suitability'] = 'very poor'

        df_trees.merge(speciesTable, how = 'left', on = 'species', sort = False)

        # save the 'data' pandas dataframe as a geodataframe
        # df_trees = gpd.GeoDataFrame(df_trees, geometry=gpd.points_from_xy(df_trees.Longitude, df_trees.Latitude)).copy() 

        # Save the inventory dates as a string.  Otherwise an error is thrown when mapping
        df_trees['date'] = df_trees['date'].astype(str)

        # get the species specific colour from the species table for each entry and create the coloursTable
        colorsTable = pd.read_excel(speciesFile,sheet_name = "colors")

        colorsTable.set_index('taxon', inplace = True)

        # st.session_state['colorsTable'] = colorsTable

        df_trees.rename(columns = {'tree_name' : 'Tree Name', 'date' : 'Date', 'block' : 'Block ID', 'tree_number' : 'Tree Number', 
                                   'house_number' : 'House Number', 'street_code' : 'Street Code', 'species_code' : 'Species Code', 
                                   'location_code' : 'Location Code', 'ownership_code' : 'Ownership Code', 
                                   'number_of_stems' : 'Number of Stems', 'dbh' : 'DBH', 'hard_surface' : 'Hard Surface', 
                                   'crown_width' : 'Crown Width', 'height_to_crown_base' : 'Ht to Crown Base', 
                                   'total_height' : 'Total Height', 'reduced_crown' : 'Reduced Crown', 
                                   'unbalanced_crown' : 'Unbalanced Crown', 'defoliation' : 'Defoliation', 
                                   'weak_or_yellow_foliage' : 'Weak or Yellowing Foliage', 
                                   'dead_or_broken_branch' : 'Dead or Broken Branch', 'lean' : 'Lean', 
                                   'poor_branch_attachment' : 'Poor Branch Attachment', 'branch_scars' : 'Branch Scars', 
                                   'trunk_scars' : 'Trunk Scars', 'conks' : 'Conks', 'branch_rot_or_cavity' : 'Rot or Cavity - Branch', 
                                   'trunk_rot_or_cavity' : 'Rot or Cavity - Trunk', 'confined_space' : 'Confined Space', 
                                   'crack' : 'Crack', 'girdling_roots' : 'Girdling Roots',  'exposed_roots' : 'Exposed Roots', 
                                   'recent_trenching' : 'Recent Trenching', 'cable_or_brace' : 'Cable or Brace', 
                                   'wire_conflict' : 'Conflict with Wires', 'sidewalk_conflict' : 'Conflict with Sidewalk', 
                                   'structure_conflict' : 'Conflict with Structure', 'tree_conflict' : 'Conflict with Another Tree', 
                                   'sign_conflict' : 'Conflict with Traffic Sign', 'comments' : 'Comments', 
                                   'longitude' : 'Longitude', 'latitude' : 'Latitude', 
                                   'street' : 'Street', 'family' : 'Family', 'genus' : 'Genus', 'species' : 'Species', 
                                   'invasivity' : 'Invasivity', 'suitability' : 'Species Suitability', 
                                   'diversity_level' : 'Diversity Level', 'native' : 'Native', 'cpa' : 'Crown Projection Area (CPA)', 
                                   'address' : 'Address', 'dbh_class' : 'DBH Class', 'rdbh' : 'Relative DBH', 
                                   'rdbh_class' : 'Relative DBH Class', 'structural' : 'Structural Defects', 
                                   'health' : 'Health Defects', 'description' : 'Description', 'defects' : 'Defects', 
                                   'defectColour' : 'Defect Colour', 'demerits' :  'Total Demerits', 'simple_rating' : 'Simple Rating'},
                                   inplace = True)
        
        if 'df_trees' not in st.session_state:

            st.session_state['df_trees'] = []

        st.session_state['df_trees'] = df_trees
            
        return df_trees

    
    if 'df_trees' not in st.session_state:

        st.session_state['df_trees'] = []

    st.session_state['df_trees'] = df_trees

    # with save_data_screen:

    #     screen1.write(df_trees.head(2))

        # save_data(df_trees)


    speciesTable = getSpeciesTable()

    with screen1:
        with st.spinner(f'### Loading your data.  Please wait'):

            df_trees = get_raw_data(fileName)
    
    df_streets = get_streets()

    with screen1:
        with st.spinner(f'### Cleaning up and deriving data.  Please wait'):

            df_trees = clean_and_expand_data(df_trees)

    # save_data(df_trees)

    return df_trees


def save_data(df_trees):
    '''Provides an option to save df_trees  AND df-streets to the same workbook'''

    # create a buffer to hold the data
    buffer = io.BytesIO()

    # create a Pandas Excel writer using the buffer
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')

    # write the dataframes to separate sheets in the workbook
    df_trees.to_excel(writer, sheet_name='trees', index=False)

    df_streets = []

    df_streets = st.session_state['df_streets']

    df_streets.to_excel(writer, sheet_name='streets', index=False)

    # save the workbook to the buffer
    writer.close()

    # reset the buffer position to the beginning
    buffer.seek(0)

    # Set timezone
    timezone = pytz.timezone('America/Toronto')

    # Get the current local time
    now = datetime.datetime.now(timezone)

    # Print the current local time
    date_time = now.strftime("%d%m%Y%H%M")

    # create a download link for the workbook
    st.download_button(

        label =':floppy_disk: Click here to save your data on your local computer',

        data=buffer,

        file_name='summary' + date_time +'.xlsx',

        mime='application/vnd.ms-excel')



fileName ='empty'

fileName = st.file_uploader("Browse for or drag and drop the name of your Neighbourwoods INPUT excel workbook", 
    type = ['xlsm', 'xlsx', 'csv'])

if fileName is not None:
    
    df_trees = create_summary_data()

    total_tree_count = df_trees.shape[0]

    st.session_state['total_tree_count'] = total_tree_count

    screen1.markdown(f'''#### There are :red[{total_tree_count}] now loaded.  You can save this summary file by clicking on the button below, and/or proceed with the analyses in the sidebar to the left''')

    

    st.dataframe(df_trees, column_config={'defectColour': None})

    with screen2:
        save_data(df_trees)

else:

    with screen1:
        st.markdown(f'''### Select a Neighbourwoods input file in the space below.''')