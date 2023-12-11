import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

# st.markdown("___")

# screen1 = st.empty()
# screen2 = st.empty()
# screen3 = st.empty()

# st.markdown("___")


def pivTable(ptab):
    """Setup a pivot table for more detailed data eexploration"""

    try:
        
        st.markdown("___")
        st.header('Pivot Table Analysis')

        numCols = st.radio('Single or Multiple Columns?', ('Single', 'Multiple'))

        ptForm = st.form(key = 'ptFunction')
        r = ptForm.selectbox('Select the row for your table', options = ptab.columns)
        
        if numCols == 'Multiple':
            c = ptForm.selectbox('Select the column for your table', options = ptab.columns)
        
        v = ptForm.selectbox('Select the value for your table', options = ptab.columns)
        f = ptForm.selectbox('Select the value for your function', options = ['sum', 'mean', 'count' ])
        
        ptForm.markdown('___')

        ptCol1, ptCol2, ptCol3, ptCol4 = ptForm.columns(4)

        showTotal = ptCol1.radio('Show column total?', ('Yes', 'No'))
        decimalNumber = ptCol2.number_input('Enter the number of decimal places for all values in table.', value  = 1)

        if f != 'mean':

            if showTotal =='Yes':
                selectMargins=True
                selectMargins_name = 'Total'
            else:
                selectMargins=False
                selectMargins_name = 'Total'

        else:

            selectMargins=False
            selectMargins_name = ''

        if f == 'count':
            f = pd.Series.nunique
            funcType = 'count'

        else: funcType = f

        ptSubmitButton = ptForm.form_submit_button("Show Pivot Table")

        if ptSubmitButton:
            
            if numCols=='Multiple':

                ptable = pd.pivot_table(ptab, 
                    index = r, 
                    columns = c, 
                    values = v, 
                    aggfunc = f,
                    margins=selectMargins,
                    margins_name=selectMargins_name)

                st.subheader(f'The {(funcType)} of {v} by {r} and {c}.')

            else:

                ptable = pd.pivot_table(ptab, 
                    index = r, 
                    values = v, 
                    aggfunc = f,
                    margins=selectMargins,
                    margins_name=selectMargins_name)

                st.subheader(f'The {(funcType)} of {v} by {r}.')

            ptable.reset_index(inplace=True)
            ptable = ptable.round(decimals = decimalNumber)

            return ptable

    except:
        st.error("Oh no!  Something went wrong.  Check to make sure that your filters in the pivot tabel setup make sense.")

try:

    pivot_table = pivTable(st.session_state['select_df'])

    if pivot_table is None:

        st.markdown(f"##### Make your selections above and then click on the 'Show Pivot Table' button.")

    else:

        st.dataframe(pivot_table)

except KeyError:

        st.error("It looks like you haven't loaded any data yet.")