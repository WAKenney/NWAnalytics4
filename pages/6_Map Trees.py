import streamlit as st
import pandas as pd

st.title("Map the Trees")

currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"

fileName ='empty'

df = pd.DataFrame()

fileName = st.file_uploader("Browse for or drag and drop the name of your Neighbourwoods SUMMAY file here",
                            type = ['xlsm', 'xlsx'], key ='fileNameKey')

@st.cache_data(show_spinner=True)
def getData(fileName):
    """Import tree data and species table and do some data organization"""

    if fileName is not None:
        df = pd.read_excel(fileName, sheet_name = "summary", header = 0)

# read the species table from the current directory which should be Github repo
speciesFile = currentDir + 'NWspecies220522.xlsx' 
speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

df = pd.read_excel(fileName, sheet_name = "summary", header = 0)

st.dataframe(df)

st.dataframe(speciesTable)

