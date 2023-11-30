import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from streamlit_folium import folium_static


#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Tree Diversity Analysis')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")

   
def diversity(data):
    """Analyze tree diversity"""

    # st.write(data.columns)

    data = data.loc[data['diversity_level'] != 'other']
   
    divLevel = st.radio('Select a level of diversity', ('species', 'genus', 'family'))
    
    st.header('Tree diversity summary by ' + divLevel)

    with st.expander("Click here to read some comments and suggestions about diversity.", expanded=False):
        st.markdown("""
            
            The first pie chart illustrates the distribution of the species, genus or family (you can select the level of diversity by selecting the 
            apporpriate radio button at the top) by the frequency or simple count of the number of trees.  But this doesn't tell the whole story. 
            A species (genus or family) could be represented by a large number of small individual trees and the first graph of simple frequency 
            would indicate that species' significance.  However, another species (genus or family) could have fewer individuals (lower frequency) 
            but of much larger size and hence a great impact on urban forest benefits.  Considering the distribution by crown projection area (cpa) 
            can reflect this potential difference.

            Crown projection area is calculated from the crown width measurements in the inventory as:
            
             cpa = 3.14*(crown width/2)^2
            
            Santamour's* often quoted "rule" of no more than 10% of the trees from one species, 
            no more than 20% from one genus and no more than 30% from one family is imperfect, but does provide some guidance with respect to "how much diversity is enough".
            With this in mind, look at the pie charts for frequency (number of trees) for species, genus and family by selectiong each of the radio buttons above to determine if
            some are over-planted.  This could help to guide planting recommendations. __Use caution when assessing filtered data!__
            
            In the following pie charts, "other" represents all species, genera or families not inccluded in the top ten making up the rest of the chart. 

            * Santamour, F.S. undated. Trees for urban planting: Diversity, uniformity, and common sense. 
            U.S. National Arboretum.  Washington D.C.).

        """)

    st.subheader('Diversity based on the number of trees (frequency)')

    if divLevel == 'species':

        st.write('Remember, the diversity analysis at the species level will NOT include any trees identified only at the genus level (e.g. pinspp, mapspp,  etc.)')
        richness =data.species.nunique()
        st.write('Keeping the above in mind, there are ', richness, 'unique species (species richness).')

        data = data.loc[(data.diversity_level == divLevel)]
    else:
        data = data.loc[(data.diversity_level != 'other')]

    totalCount = len(data.index)
    topTenSpecies = data.loc[: , [divLevel, 'tree_name']]
    topTenSpeciesPT = pd.pivot_table(topTenSpecies, index=[divLevel], aggfunc='count')
    topTenSpeciesPT.reset_index(inplace=True)
    topTenSorted = topTenSpeciesPT.sort_values(by='tree_name',ascending=False).head(10)
    topTenTotal = topTenSorted['tree_name'].sum()
    otherTotal = totalCount - topTenTotal

    # initialize list for 'other' row iin table 
    other_data = [['Other', otherTotal]] 
    
    # Create the pandas DataFrame of 'other' row
    other_df = pd.DataFrame(other_data, columns=[divLevel, 'tree_name'])

    #concatenate the full table and the row for 'other'
    topTenPlusOther = pd.concat([topTenSorted,other_df])

    #rename the column named 'tree-name' to frequency. 'tree-name' was used to count since every rows is sure to have a value in  tree name
    topTenPlusOther.rename(columns = {'tree_name': 'frequency'},inplace = True)

    speciesPie = px.pie(topTenPlusOther, 
        values='frequency', 
        names = divLevel,
        
        )

    # speciesPie = px.pie(topTenPlusOther, 
    #     values='frequency', 
    #     names = divLevel,
    #     color = divLevel,
    #     color_discrete_map = colorsDict
    #     )

    speciesPie.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    speciesPie.update_layout(showlegend=False)
    speciesPie.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    

    with st.expander("Click to view tabular data.", expanded=False):
        divTable = ff.create_table(topTenPlusOther.round(decimals = 0))
        st.plotly_chart(divTable)

    st.plotly_chart(speciesPie)
    
    st.subheader('Diversity based on crown projection area (CPA)')
    
    totalCpa = data['cpa'].sum()
    
    topTenCpa = data.loc[: , [divLevel, 'cpa']]
    topTenCpaPT = pd.pivot_table(topTenCpa, index=[divLevel], aggfunc='sum')
    topTenCpaPT.reset_index(inplace=True)
    topTenCpaSorted = topTenCpaPT.sort_values(by='cpa',ascending=False).head(10)
    topTenCpaTotal = topTenCpaSorted['cpa'].sum()
    otherCpaTotal = totalCpa - topTenCpaTotal
    topTenCpaPlusOther = topTenCpaSorted.append({divLevel:'Other', 'cpa': otherCpaTotal}, ignore_index =True)
    topTenCpaPlusOther.rename(columns = {'cpa': 'Crown Projection Area'},inplace = True)
    
    CpaPie = px.pie(topTenCpaPlusOther, 
        values='Crown Projection Area', 
        names = divLevel,
        color = divLevel,
        color_discrete_map = colorsDict
        )

    CpaPie.update_traces(insidetextorientation='radial', textinfo='label+percent') 
    CpaPie.update_layout(showlegend=False)
    CpaPie.update_traces(textfont_size=15,
                  marker=dict(line=dict(color='#000000', width=1)))
    
    st.plotly_chart(CpaPie)
    
diversity(st.session_state.select_df)