import pandas as pd
import geopandas as gpd
import streamlit as st
import io
# from io import BytesIO
import base64


df_trees = pd.DataFrame()

st.title('Neighbourwoods Data Entry and Clean-up')

st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"

speciesFile = currentDir + 'NWspecies220522.xlsx'


@st.cache_data(show_spinner="Loading the species table, please wait ...")
def getSpeciesTable(): 
    speciesTable = pd.read_excel(speciesFile,sheet_name = "species")
    return speciesTable

speciesTable = getSpeciesTable()

activeEcodist = '6E-16'

attributeNames = ['reduced_crown', 'unbalanced_crown', 'defoliation',
    'weak_or_yellow_foliage', 'dead_or_broken_branch',  'lean', 'poor_branch_attachment',	
    'branch_scars', 'trunk_scars', 'conks', 'branch_rot_or_cavity', 
    'trunk_rot_or_cavity', 'confined_space', 'crack', 'exposed_roots', 'girdling_roots', 'recent_trenching']

fileName ='empty'

fileName = st.file_uploader("Browse for or drag and drop the name of your Neighbourwoods INPUT excel workbook", 
    type = ['xlsm', 'xlsx', 'csv'], 
    key ='fileNameKey')

@st.cache_data(show_spinner="Loading your data, please wait ...")
def getData(fileName):

    if fileName is not None:

        df_trees = pd.DataFrame()
        df_streets = pd.DataFrame()

        try:
            # df_trees = pd.read_excel(fileName, sheet_name = 'trees', header = 0)
            df_trees = pd.read_excel(fileName, sheet_name = 0, header = 0)
        except:
            st.error("Ooops something is wrong with your data file!")

        return df_trees
    
df_trees = getData(fileName)


@st.cache_data(show_spinner="Loading your street data, please wait ...")
def get_streets():
    # df_streets = pd.read_excel(fileName, sheet_name = 'streets', header = 0)
    # if df_streets.iat[0,0] == 'street_code':
    #     df_streets = pd.read_excel(fileName, sheet_name = 'streets', header = 1)
    # if df_streets.iat[0,0] == 'street':
    #     df_streets = pd.read_excel(fileName, sheet_name = 'streets', header = 1)

    df_streets = pd.read_excel(fileName, sheet_name = 1, header = 0)
    if df_streets.iat[0,0] == 'street_code':
        df_streets = pd.read_excel(fileName, sheet_name = 1, header = 1)
    if df_streets.iat[0,0] == 'street':
        df_streets = pd.read_excel(fileName, sheet_name = 1, header = 1)


    return df_streets

df_streets = get_streets()

df_trees.rename(columns = {'Tree Name':'tree_name','Date':'date','Block Id':'block','Block ID':'block','Tree No':'tree_number',
                        'House Number':'house_number',
                        'location':'location_code','Location Code':'location_code',
                        'ownership':'ownership_code','Ownership code':'ownership_code', 'Ownership Code':'ownership_code',
                        'Crown Width':'crown_width','Number of Stems':'number_of_stems','DBH':'dbh',
                        'Hard surface':'hard_surface','Hard Surface':'hard_surface','Ht to base':'height_to_crown_base',
                        'Total Height':'total_height','Reduced Crown':'reduced_crown','Unbalanced Crown':'unbalanced_crown',
                        'Defoliation':'defoliation','Weak or Yellow Foliage':'weak_or_yellow_foliage','Weak or Yellowing Foliage':'weak_or_yellow_foliage',
                        'Dead or Broken Branch':'dead_or_broken_branch','Lean':'lean','Poor Branch Attachment':'poor_branch_attachment',
                        'Branch Scars':'branch_scars','Trunk Scars':'trunk_scars','Conks':'conks','Rot or Cavity - Branch':'branch_rot_or_cavity',
                        'Rot or Cavity - Trunk':'trunk_rot_or_cavity','Confined Space':'confined_space',
                        'Crack':'crack','Girdling Roots':'girdling_roots', 'Exposed Roots': 'exposed_roots', 'Recent Trenching':'recent_trenching',
                        'Cable or Brace':'cable_or_brace','Conflict with Wires':'wire_conflict',
                        'Conflict with Sidewalk':'sidewalk_conflict','Conflict with Structure':'structure_conflict',
                        'Conflict with another tree':'tree_conflict','Conflict with Traffic Sign':'sign_conflict'}, inplace = True)

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

# def getSpeciesTable(): 
#     speciesTable = pd.read_excel(speciesFile,sheet_name = "species")
#     return speciesTable

# speciesTable = getSpeciesTable()

def getOrigin():
    origin = pd.read_excel(speciesFile, sheet_name = 'origin')

    return origin

df_origin = getOrigin()

def getEcodistricts():
    gpd_ecodistricts = gpd.read_file(r"https://github.com/WAKenney/NWAnalytics/blob/master/OntarioEcodistricts.gpkg")
    return gpd_ecodistricts

# gpd_ecodistricts = getEcodistricts()

def getCodes():
    codes = pd.read_excel(speciesFile, sheet_name = 'codes')
    return codes

df_codes = getCodes()

df_trees = df_trees.merge(speciesTable.loc[:,['species_code','family', 'genus','species', 'Max DBH', 'invasivity',
    'suitability', 'diversity_level']], how='left')

df_trees=df_trees.rename(columns = {'Max DBH':'max_dbh'})

def origin(df_trees):
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

# df_trees['Structural Defect']= df_trees.apply(structural, axis =1)
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

# df_trees['Health Defect']= df_trees.apply(health, axis =1)
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



####################################

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


#####################################

df_trees.rename(columns = {'tree_name':'Tree Name', 'date': 'Date', 'block':'Block ID',
    'Tree No':'Tree Number','street_name':'Street','location_code': 'Location Code','ownership_code': 'Ownership Code',
    'crown_width': 'Crown Width','number_of_stems':'Number of Stems','dbh':'DBH',
    'hard_surface':'Hard Surface','height_to_crown_base': 'Ht to Crown Base', 'total_height':'Total Height',
    'reduced_crown':'Reduced Crown','unbalanced_crown':'Unbalanced Crown',
    'defoliation':'Defoliation','weak_or_yellow_foliage':'Weak or Yellowing Foliage','dead_or_broken_branch':'Dead or Broken Branch',
    'lean':'Lean','poor_branch_attachment':'Poor Branch Attachment','branch_scars':'Branch Scars','trunk_scars':'Trunk Scars',
    'conks':'Conks','branch_rot_or_cavity':'Rot or Cavity - Branch','trunk_rot_or_cavity':'Rot or Cavity - Trunk',
    'confined_space':'Confined Space','crack':'Crack','girdling_roots':'Girdling Roots', 'exposed_roots':'Exposed Roots',
    'recent_trenching':'Recent Trenching','cable_or_brace':'Cable or Brace','wire_conflict':'Conflict with Wires',
    'sidewalk_conflict':'Conflict with Sidewalk','structure_conflict':'Conflict with Structure',
    'tree_conflict':'Conflict with Another Tree','sign_conflict':'Conflict with Traffic Sign', 'family':'Family',
    'genus':'Genus', 'species':'Species', 'Relative Dbh': 'Relative DBH', 'origin':'Native', 'suitability':'Species Suitability',
    'diversity_level':'Diversity Level','invasivity':'Invasivity','X coordinate':'Longitude', 'Y coordinate':'Latitude'
    }, inplace = True)

if df_trees not in st.session_state:
    st.session_state['df_trees'] = []

st.session_state['df_trees'] = df_trees

st.dataframe(df_trees)


#Option to save the data checking table as a spreadsheet
towrite = io.BytesIO()
downloaded_file = df_trees.to_excel(towrite, index=False, header=True, sheet_name = 'summary')
towrite.seek(0)  # reset pointer
b64 = base64.b64encode(towrite.read()).decode()  # some strings
linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="summary data.xlsx">Click here to save your data as an Excel file</a>'
st.markdown(linko, unsafe_allow_html=True)





#####################################


# def fixTitles():

#     #  Column titles from the Neighourwoods MS 2.6 workbook
#     nwWkbkTitles = ['tree index','Tree name', 'Date', 'Block Id', 'Tree No', 'House Number', 'street_code', 'species_code', 'location_code', 
#     'ownership_code', 'Number of Stems', 'DBH', 'Hard surface', 'Crown Width', 'Ht to base', 'Total Height', 'Reduced Crown', 
#     'Unbalanced Crown', 'Defoliation', 'Weak or Yellow Foliage', 'Dead or Broken Branch', 'Lean', 'Poor Branch Attachment', 
#     'Branch Scars', 'Trunk Scars', 'Conks', 'Rot or Cavity - Branch', 'Rot or Cavity - Trunk', 'Confined Space', 'Crack', 
#     'Girdling Roots', 'Exposed Roots', 'Recent Trenching', 'Cable or Brace', 'Conflict with Wires', 'Conflict with Sidewalk', 
#     'Conflict with Structure', 'Conflict with another tree', 'Conflict with Traffic Sign', 'Comments', 'X coordinate', 'Y coordinate']

#     #  Column titles from the Neighourwoods Memento data entry library
#     mementoTitles = ['Tree name', 'Date', 'Block Id', 'Tree No', 'House Number', 'street_code', 'species_code', 'location', 
#     'ownership', 'Number of Stems', 'DBH', 'Hard surface', 'Crown Width', 'Ht to base', 'Total Height', 'Reduced Crown', 
#     'Unbalanced Crown', 'Defoliation', 'Weak or Yellow Foliage', 'Dead or Broken Branch', 'Lean', 'Poor Branch Attachment', 
#     'Branch Scars', 'Trunk Scars', 'Conks', 'Rot or Cavity - Branch', 'Rot or Cavity - Trunk', 'Confined Space', 'Crack', 
#     'Girdling Roots', '', 'Recent Trenching', 'Cable or Brace', 'Conflict with Wires', 'Conflict with Sidewalk', 
#     'Conflict with Structure', 'Conflict with another tree', 'Conflict with Traffic Sign', 'Comments', 'xy', 'Photo 1', 'Photo 2']

#     #  Column titles from the Neighbourwoods_Data_ENTRY_141221.xlsm workbook
#     nwInputTitles = ['Date(dd/mm/yy)', 'Block', 'Tree No', 'House Number', 'Street Code', 'Species Code', 'Location Code', 
#     'Ownership Code', 'No. of Stems', 'DBH (cm)', '% Hard surface', 'Crown Width (m)', 'Ht to base of crown.', 'Total Height (m)', 'Reduced Crown', 
#     'Unbalanced Crown', 'Defoliation', 'Weak or Yellow Foliage', 'Dead or Broken Branch', 'Lean', 'Poor Branch Attachment', 
#     'Branch Scars', 'Trunk Scars', 'Conks', 'Rot or Cavity - Branch', 'Rot or Cavity - Trunk', 'Confined Space', 'Crack', 
#     'Girdling Roots', 'Recent Trenching', 'Exposed Roots', 'Cable or Brace', 'Conflict with Wires', 'Conflict with Sidewalk', 
#     'Conflict with Structure', 'Conflict with another tree', 'Conflict with Traffic Sign', 'Comments', 'X coordinate', 'Y coordinate']

#     dfTitles = df_trees.columns

#     for nwWkbkTitle in nwWkbkTitles:
#         if nwWkbkTitle not in dfTitles:
#             st.warning("Ooops ", nwWkbkTitle, " isn't a column in your dataset!")

#         if inputType == 'Neighourwoods Memento data entry library':
#             st.info ('You have selected "Neighourwoods Memento data entry library" as your input data type')
#     else:
#         st.info ('You have selected "Neighbourwoods_Data_ENTRY.xlsm workbook" as your input data type')    
