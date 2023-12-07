import pandas as pd
import geopandas as gpd
import streamlit as st

st.write(st.session_state)

if 'df_trees' not in st.session_state:

        st.write('df-trees is not loaded yet')

st.write(st.session_state.df_trees.columns)

