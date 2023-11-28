import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Tree Ownership Analysis')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")