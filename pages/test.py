import io
import pandas as pd
import geopandas as gpd
import streamlit as st
from shapely.geometry import Point
import folium
from streamlit_folium import folium_static
import datetime
import pytz

from random import randint


def save_data(df):
    '''Provides an option to save df_trees  AND df-streets to the same workbook'''

    # create a buffer to hold the data
    buffer = io.BytesIO()

    # create a Pandas Excel writer using the buffer
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')

    # write the dataframes to separate sheets in the workbook
    df.to_excel(writer, index=False)

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

        file_name='output' + date_time +'.xlsx',

        mime='application/vnd.ms-excel')




# currentDir = "https://raw.githubusercontent.com/WAKenney/NWAnalytics/master/"

# speciesFile = currentDir + 'NWspecies220522.xlsx'

# speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

# st.write(speciesTable.head(2))

# speciesTable['color'] = speciesTable['color'].apply(lambda x : '#%06x' % randint(0, 0xFFFFFF))

# st.write(speciesTable.head(2))

# save_data(speciesTable)

speciesFile = 'NWspecies220522.xlsx'

speciesTable = pd.read_excel(speciesFile,sheet_name = "species")

st.dataframe(speciesTable)