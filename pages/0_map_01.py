import folium
import streamlit as st
from streamlit_folium import st_folium, folium_static
import leafmap.foliumap as leafmap

from pages.floodmap import *

st.set_page_config(layout="wide")


"""
# 极端事件--寒潮

## 技术难点

- 地图交互

  > `st_folium`响应非常缓慢

- 对接R语言`ggplot2`绘图
"""

# 获取所有站点
# db = DataBase()  # auto login
# stationInfo = db.read_table("st_daily_met2481")

@st.cache_resource
def load_data():
    return pd.read_csv("data/st_2481.csv")

stationInfo = load_data()

cug_new = [30.46001618003947, 114.61223316513498]
cug_old = [30.46001618003947, 114.61223316513498]

zoom_start=11

@st.cache_resource
def addLayer_base():
    # m = folium.Map(location=loc_cug, zoom_start=16)
    m = leafmap.Map(location=cug_new, zoom_start=zoom_start)
    return m

def add_Marker(loc, label):
    kw = {"prefix": "fa", "color": "green", "icon": "arrow-up"}
    angle = 180
    icon = folium.Icon(angle=angle, **kw)
    return folium.Marker(loc, icon=icon, tooltip=label)


# star_icon = folium.Icon(icon='star', prefix='fa', color='blue')

@st.cache_resource
def add_FeatureGroup():
    fg = folium.FeatureGroup(name="State bounds")
    # p1 = add_Marker(cug_old, "cug_old")
    # p2 = add_Marker(cug_new, "cug_new")
    # fg.add_child(p1)
    # fg.add_child(p2)

    points_met = add_points_from_xy(stationInfo, x="lon", y="lat", layer_name="sites")
    fg.add_child(points_met)
    return fg

fg = add_FeatureGroup()


# points_met = None
m = addLayer_base()


if st.button("Reset"):
    m = leafmap.Map(location=cug_new, zoom_start=zoom_start)

# fg.add_to(m)
# m.add_child(fg)
m.add_points_from_xy(stationInfo, x="lon", y="lat", layer_name="sites")
m.to_streamlit(height=800)

col1, col2 = st.columns([4, 1])
# returned_objects=["last_object_clicked", "last_clicked"]
# with col1:
#     st_data = st_folium(m, height=800, width = 1500, 
#                         returned_objects=["last_object_clicked"], 
#                         feature_group_to_add=fg) # "last_object_clicked"
# with col2:
#     st_data


# 寒潮部分
"""
## 1. 查询数据
"""

sites = stationInfo["name"].to_list()

"### 站点信息"
site = st.selectbox("请选择一个站点", sites, index=sites.index(sites[0]))
stationInfo[stationInfo.name == site]

"### 站点数据"
table = "China_Mete2000_daily_1951_2019"
table = "China_Mete2000_daily_2020_2022"

# df = db.read_table(table, site)

# # 简单的绘图
# st.line_chart(
#     df,
#     x='date',
#     y=["TEM_Min"]
# )

# df
