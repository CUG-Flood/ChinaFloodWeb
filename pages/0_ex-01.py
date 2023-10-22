import folium
import folium as fl
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
from pages.floodmap import *
import asyncio
import time


st.set_page_config(layout="wide")


@st.cache_resource
def load_data():
  df = pd.read_csv("data/st_2481.csv")
  return df.loc[:, ["name", "prov", "lon", "lat"]] # "site", "prov", 


stationInfo_all = load_data().iloc[0:2400] # 1500个站点能抗住


"## 选择省份"
provs = stationInfo_all.prov.unique().tolist()
print(provs)

prov = st.selectbox("请选择省份", provs, index=provs.index("湖北"))
stationInfo = stationInfo_all[stationInfo_all.prov == prov]
n = stationInfo.shape[0]
f"{prov}共{n}个站点"


sites = stationInfo["name"].to_list()
site0 = sites[0]
# site0 = "武汉"

"### 站点信息"
site = st.selectbox("请选择一个站点", sites, index=sites.index(site0))
d = stationInfo[stationInfo.name == site]
d

loc = get_site_loc(d)
# map["last_object_clicked_tooltip"]

# TODO: 先添加一个功能过滤省份
c1, _,  c2 = st.columns([3, 1, 3])
with c1:
  zoom_value = st.slider('Zoom level', 1, 18, 10)

with c2:
  if st.button("Reset Map"):
    "reset map"


m = fl.Map(location=loc, zoom_start=zoom_value)
# m.add_child(fl.LatLngPopup())

fg, points = add_FeatureGroup(stationInfo)
p = add_Marker(loc, site, {"color": "red"})
fg.add_children([p, cug_old, cug_new])

# m.add_children([fg])
# when zoom changes update slider too

# st.session_state


async def draw_async():
  c0, c1, c2 = st.columns([4, 1, 0.2])
  # , "last_object_clicked_popup"
  events = ["last_object_clicked_tooltip"] # , "last_object_clicked_popup"
  # "last_object_clicked", "last_clicked", 
  with c0:
    # st_folium is low performance, how to improve?
    t0 = time.time()
    
    map = st_folium(m, feature_group_to_add=fg,
                    returned_objects=events, height=700, width="100%")
    print("--- %s seconds ---" % (time.time() - t0))

  # with c1:
  #   map

## 异步并未发挥作用
try:
  # async run the draw function, sending in all the
  # widgets it needs to use/populate
  asyncio.run(draw_async())
  
except Exception as e:
  print(f'error...{type(e)}')
  raise
finally:
  # some additional code to handle user clicking stop
  print('finally')
  
# map_click = map["last_clicked"]
# map_click
# TODO: 添加所有的点

# 猜测哪个点被选择了，然后进行绘图
# get_click_pos(map['last_clicked'])
