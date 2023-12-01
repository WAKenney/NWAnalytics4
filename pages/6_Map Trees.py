import folium
from folium.plugins import Fullscreen
import streamlit as st
from streamlit_folium import folium_static

#Create page title
titleCol1, titleCol2, titleCol3 =st.columns((1,4,1))

title = 'new_nw_header.png'

titleCol2.image(title, use_column_width=True)

st.subheader('Map the Trees')

st.markdown("___")

screen1 = st.empty()
screen2 = st.empty()
screen3 = st.empty()

st.markdown("___")

main_screen = st.empty()

def mapItFolium(mapData):

    '''Generates a folium map using the selected dataframe
    '''

    pointSizeSlider = st.slider('Move the slider to adjust the point size', min_value = 2, max_value = 20, value =4)
        
    # if mapData is None:
    #     st.warning("Be sure to finish selecting the filtering values in the sidebar to the left.")

    # Drop entries with no latitude or longitude values entered
    mapData = mapData[mapData['latitude'].notna()] 
    mapData = mapData[mapData['longitude'].notna()]

    mapData['crown_radius'] = mapData['crown_width']/2

    #calculate the average Latitude value and average Longitude value to use to centre the map
    # avLat = mapData['latitude'].mean()  
    # avLon = mapData['longitude'].mean()
    
    #calculate the avergae lat and lon for centering the map and the max and min values to set the bounds of the map
    # avLat=st.session_state('avLat')
    # avLon=st.session_state('avLat')
    maxLat=mapData['latitude'].max()
    minLat=mapData['latitude'].min()
    maxLon=mapData['longitude'].max()
    minLon=mapData['longitude'].min()
    
    #setup the map
    treeMap = folium.Map(location=[st.session_state['avLat'], st.session_state['avLon']],  
        zoom_start=5,
        max_zoom=100, 
        min_zoom=1, 
        width ='100%', height = '100%', 
        prefer_canvas=True, 
        control_scale=True,
        tiles='OpenStreetMap'
        )

    treeMap.fit_bounds([[minLat,minLon], [maxLat,maxLon]])

    mapData.apply(lambda mapData:folium.CircleMarker(location=[mapData["latitude"], mapData["longitude"]], 
        color='white', # use a white border on the circle marker so it will show up on satellite image
        stroke = True,
        weight = 1,
        fill = True,
        fill_color=mapData['defectColour'],
        fill_opacity = 0.6,
        line_color='#000000',
        radius= pointSizeSlider, #setup a slide so the use can chage the size of the marker
        tooltip = mapData['tree_name'],
        popup = folium.Popup(mapData["description"], 
        name = "Points",
        max_width=450, 
        min_width=300)).add_to(treeMap), 
        axis=1)

    #have an ESRI satellite image as an optional base map
    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Satellite',
        overlay = False,
        control = True
       ).add_to(treeMap)

    # add a fullscreen option and layer control to the map
    Fullscreen().add_to(treeMap)
    folium.LayerControl().add_to(treeMap)
    
    # Show the map in Streamlit

    folium_static(treeMap)

    #Add the legend saved at github called mapLegend.png
    # st.image(currentDir + 'mapLegend.png')


if st.session_state['select_df'] is not None:
      
    if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

        screen1.markdown(f"#### The map shows the :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

        mapItFolium(st.session_state['select_df'])

    else:

        screen1.markdown(f"#### The map shows ALL :red[{st.session_state['total_tree_count']}] entries. ")

        mapItFolium(st.session_state['select_df'])

else:

    st.error("Load data")


# if st.session_state['df_trees'] is not None:
    
mapItFolium(st.session_state['select_df'])

# else:

#     screen1.markdown("You still haven't loaded your data!")

# if "select_df" in st.session_state:
      
#     if st.session_state['total_tree_count'] != st.session_state['select_tree_count']:

#         screen1.markdown(f"#### The map shows the :red[{st.session_state['select_tree_count']}] entries in the filtered data. ")

#         mapItFolium(st.session_state['select_df'])

#     else:

#         screen1.markdown(f"#### The map shows ALL :red[{st.session_state['total_tree_count']}] entries. ")
#         mapItFolium(st.session_state['select_df'])

# else:

#     mapItFolium(st.session_state['select_df'])
