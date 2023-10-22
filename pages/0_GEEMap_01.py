# %%
# import geemap
import numpy as np
import geemap.foliumap as geemap
import ee
import streamlit as st

st.set_page_config(layout="wide")
ee.Initialize()

"""
# Landsat 9 land surface temperature in Wuhan, China
"""

# %%
def unique(x):
  return np.unique(np.array(x)).tolist()


def ee_date_format(x):
  return ee.Date(x).format("YYYY-MM-dd")


def addProbDate(img):
  date = img.get("system:time_start")
  datestr = ee_date_format(date)
  return img.set('date', datestr)


def Tland_decode(img):
  r = img.expression("b('ST_B10') * 0.00341802 + 149 - 273.15").rename("Tland")
  return ee.Image(r.copyProperties(img, img.propertyNames()))


@st.cache_data
def get_ls9_Tland(year):
  ls9 = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
  poly = ee.FeatureCollection("users/kongdd/shp_basins/poly_Hubei_Wuhan")

  filter = ee.Filter.calendarRange(year, year, "year")
  col = (ls9.filterBounds(poly).filter(filter)
         .map(addProbDate)
         )
  n = col.size().getInfo() # how many images
  st.write(f"found {n} images ")

  col_Tland = col.map(Tland_decode)

  dates = col_Tland.aggregate_array("date").getInfo()
  dates = unique(dates)
  return col_Tland, dates


# year = st.slider('year', 2021, 2023, 2022)
year = 2022
col, dates = get_ls9_Tland(year)

# %%
date = st.selectbox("Date", dates)
# date = dates[0]
img = col.filterMetadata("date", "equals", date)
# img
# %%
# 绘图
cols = [
    "#FF1493", "#FFB6C1", "#B22222", "#FF4500", "#FFA500", "#FFE100", "#DEB887", "#F5E6BE", "#2E8B57", "#9ACD32", "#20B2AA", "#B0E0E6", "#789BF2", "#3C64E6", "#0000C8", "#9370DB"]
cols.reverse()
# cols

vis = {"min": 0, "max": 50, "palette": cols}

Map = geemap.Map()
Map.addLayer(img, vis, "Tland")
Map.centerObject(img.geometry(), 9)

Map.add_colorbar(vis, label="Land Surface Temperature (℃)",
                 position="topright",
                 layer_name="Tland", font_size=9)

# Map.add_time_slider(col_Tland, vis, time_interval=1) # not work in st
# Map

# %%
Map.to_streamlit()

# %%

"""
## TODO

1. 运行速度比较慢
   > `st_cache`能否缓解？

2. 未添加除云的功能
   > js to python
"""
