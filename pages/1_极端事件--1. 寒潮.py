import folium
import streamlit as st
from streamlit_folium import st_folium
# import leafmap.foliumap as leafmap

from floodmap import *

"""
# 极端事件--寒潮
"""

# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)
st_data

## 寒潮部分

"""
## 1. 查询数据
"""
db = DataBase()  # auto login

## 所有站点
stationInfo = db.read_table("st_daily_met2481")
sites = stationInfo["site"].to_list()

"### 站点信息"
site = st.selectbox("请选择一个站点", sites, index=sites.index(sites[0]))
stationInfo[stationInfo.site == site]

"### 站点数据"
df = db.read_table("China_Mete2000_daily_1951_2019", site)
# df = query_data_site(cursor, )
df

## 简单的绘图
st.line_chart(
    df,
    x='date',
    y=["Tair_min"]
)
