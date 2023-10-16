# %%
# import folium
# from folium import Map, Marker
from ipyleaflet import *
import ipyleaflet
from ipyleaflet import leaflet

# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium, folium_static
# st.set_page_config(layout="wide")
# %%
from pages.floodmap import *

# # 获取所有站点
# db = DataBase()  # auto login
# stationInfo = db.read_table("st_daily_met2481")

# stationInfo.to_csv("st_2481.csv", index=False)
# db.close()

df = pd.read_csv("st_2481.csv")
df

points = []

for i in range(0, len(df.index)):
    i = - 1
    d = df.iloc[i]
    p = (d.lat, d.lon)
    points.append(p)

points
# %%

def point_click(event, type, coordinates):
    print(event, type, coordinates)

def add_markers(m):
    
    markers = []
    for i in range(len(points)):
        new_marker_loc = (points[i][0], points[i][1])
        new_marker = Marker(location=new_marker_loc, draggable=False)

        new_marker.on_click(point_click)
        markers.append(new_marker)
    
    cluster = MarkerCluster(markers=markers)
    # print(cluster)
    m.add_layer(cluster)
    return m

# map = L.Map(center=(51.476852, -0.000500), zoom=12, scroll_wheel_zoom=True)
# Add a distance scale

capitol_loc = (30, 110)
map = ipyleaflet.Map(center=(capitol_loc), zoom=5) 
map.add_control(leaflet.ScaleControl(position="bottomleft"))

map = add_markers(map)
map

# map
