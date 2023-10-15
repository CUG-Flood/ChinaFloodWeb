import folium
import streamlit as st
from streamlit_folium import st_folium, folium_static
import leafmap.foliumap as leafmap

from floodmap import *

st.set_page_config(layout="wide")


"""
# 极端事件--寒潮
"""

# 获取所有站点
db = DataBase()  # auto login
stationInfo = db.read_table("st_daily_met2481")


cug_new = [30.46001618003947, 114.61223316513498]
cug_old = [30.46001618003947, 114.61223316513498]


@st.cache_resource
def addLayer_base():
    # m = folium.Map(location=loc_cug, zoom_start=16)
    m = leafmap.Map(location=cug_new, zoom_start=13)
    return m


fg = folium.FeatureGroup(name="State bounds")
fg.add_child(folium.Marker(cug_old, popup="cug_old", tooltip="cug_old"))
fg.add_child(folium.Marker(cug_new, popup="cug_new", tooltip="cug_new"))

points_met = add_points_from_xy(stationInfo, x="lon", y="lat", layer_name="sites")
fg.add_child(points_met)

# points_met = None
m = addLayer_base()

# m.to_streamlit(height=800)

col1, col2 = st.columns(2)

with col1:
    st_data = st_folium(m, height=800, width = 1500, feature_group_to_add=fg, 
                        returned_objects=["last_object_clicked"])
with col2:
    st_data


# 寒潮部分
"""
## 1. 查询数据
"""

sites = stationInfo["site"].to_list()

"### 站点信息"
site = st.selectbox("请选择一个站点", sites, index=sites.index(sites[0]))
stationInfo[stationInfo.site == site]

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
