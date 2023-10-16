import folium
import streamlit as st
from streamlit_folium import st_folium
import leafmap.foliumap as leafmap
import pandas as pd
from pages.floodmap import *

st.set_page_config(layout="wide")

zoom_start=11

cug_new = [30.46001618003947, 114.61223316513498]
cug_old = [30.46001618003947, 114.61223316513498]
# fg, points_met = add_FeatureGroup()
p_new = add_Marker(cug_new, "cug_new")
p_old = add_Marker(cug_old, "cug_old")


# @st.cache_data
def load_data():
    return pd.read_csv("data/st_2481.csv")

stationInfo = load_data()

# 寒潮部分
"""
## 1. 查询数据
"""

sites = stationInfo["name"].to_list()

"### 站点信息"
site = st.selectbox("请选择一个站点", sites, index=sites.index(sites[0]))
d = stationInfo[stationInfo.name == site]
d

"### 站点数据"
table = "China_Mete2000_daily_1951_2019"
table = "China_Mete2000_daily_2020_2022"

def get_loc(site):
    d = stationInfo[stationInfo.name == site]
    return [d.lat, d.lon]

p = get_loc(site)
print(p)


# @st.cache_data
def add_Marker(loc, label):
    kw = {"prefix": "fa", "color": "green", "icon": "arrow-up"}
    angle = 180
    icon = folium.Icon(angle=angle, **kw)
    return folium.Marker(loc, icon=icon, tooltip=label)

# @st.cache_data


# fg, points_met = add_FeatureGroup()
p_new = add_Marker(cug_new, "cug_new")
p_old = add_Marker(cug_old, "cug_old")


def basemap():
    loc = [30.46001618003947, 114.61223316513498]
    loc[0] = p[0]
    loc[1] = p[1]
    
    m = leafmap.Map(location=loc, zoom_start=14)
    # points_met.add_to(m)
    # p_new.add_to(m)
    m.to_streamlit(height=600)


# loc = get_loc()
# print(loc)
col1, col2 = st.columns([4, 1])
basemap()

# with col1:
#     # m = folium.Map(location=loc_cug, zoom_start=16)
#     # Map.add_xy_data(stationInfo, x="lon", y="lat", layer_name="sites")
#     basemap(site)
# basemap(site)

  
  # st_data = st_folium(m, width=1200)
# with col2:
#   # st_data

