# https://github.com/opengeos/leafmap/blob/a76d49ba6120acce6afbdc62e3fad37823f92f54/leafmap/foliumap.py#L2154
from typing import *
import pandas as pd
import folium
from folium import Map, plugins
import streamlit as st


def get_click_pos(e):
  if e is not None:
    return e["lat"], e["lng"]
  else:
    return "No click"


def get_site_loc(d):
  d0 = d.iloc[0]
  return [d0.lat, d0.lon]


# folium.Map.add_children()
def add_children(self, children):
  for x in children:
    self.add_child(x)

# rewrite function
Map.add_children = add_children
folium.FeatureGroup.add_children = add_children


@st.cache_data
@st.cache_resource
def add_FeatureGroup(df, group_name="site_group"):
  """
  fg, points = add_FeatureGroup(df)
  """
  fg = folium.FeatureGroup(name=group_name)
  points = add_points_from_xy(df, x="lon", y="lat", layer_name="sites", popup=["name"])
  fg.add_child(points)
  return fg, points



# @st.cache_data
def add_Marker(loc, label, kw={"prefix": "fa", "color": "green", "icon": "arrow-up"}):
  if kw is not None:
    angle = 180
    icon = folium.Icon(angle=angle, **kw)
    return folium.Marker(loc, icon=icon, tooltip=label)
  else:
    return folium.Marker(loc, tooltip=label)


def add_points_from_xy(
    data: Union[str, pd.DataFrame],
    x: Optional[str] = "longitude",
    y: Optional[str] = "latitude",

    popup: Optional[List] = None,
    min_width: Optional[int] = 100,
    max_width: Optional[int] = 200,

    layer_name: Optional[str] = "Marker Cluster",
    color_column: Optional[str] = None,

    marker_colors: Optional[List] = None,
    icon_colors: Optional[List] = ["white"],
    icon_names: Optional[List] = ["info"],
    angle: Optional[int] = 0,
    prefix: Optional[str] = "fa",
    add_legend: Optional[bool] = True,
    max_cluster_radius: Optional[int] = 80,
    **kwargs,
):
  """Adds a marker cluster to the map.

  Args:
      data (str | pd.DataFrame): A csv or Pandas DataFrame containing x, y, z values.
      x (str, optional): The column name for the x values. Defaults to "longitude".
      y (str, optional): The column name for the y values. Defaults to "latitude".

      popup (list, optional): A list of column names to be used as the popup. Defaults to None.
      
      min_width (int, optional): The minimum width of the popup. Defaults to 100.
      max_width (int, optional): The maximum width of the popup. Defaults to 200.
      layer_name (str, optional): The name of the layer. Defaults to "Marker Cluster".
      color_column (str, optional): The column name for the color values. Defaults to None.
      marker_colors (list, optional): A list of colors to be used for the markers. Defaults to None.
      icon_colors (list, optional): A list of colors to be used for the icons. Defaults to ['white'].
      icon_names (list, optional): A list of names to be used for the icons. More icons can be found
          at https://fontawesome.com/v4/icons or https://getbootstrap.com/docs/3.3/components/?utm_source=pocket_mylist. Defaults to ['info'].
      angle (int, optional): The angle of the icon. Defaults to 0.
      prefix (str, optional): The prefix states the source of the icon. 'fa' for font-awesome or 'glyphicon' for bootstrap 3. Defaults to 'fa'.
      add_legend (bool, optional): If True, a legend will be added to the map. Defaults to True.
      max_cluster_radius (int, optional): The maximum radius that a cluster will cover from the central marker (in pixels).
      **kwargs: Other keyword arguments to pass to folium.MarkerCluster(). For a list of available options,
          see https://github.com/Leaflet/Leaflet.markercluster. For example, to change the cluster radius, use options={"maxClusterRadius": 50}.
  """

  if "maxClusterRadius" not in kwargs:
    kwargs["maxClusterRadius"] = max_cluster_radius

  color_options = [
      "red",
      "blue",
      "green",
      "purple",
      "orange",
      "darkred",
      "lightred",
      "beige",
      "darkblue",
      "darkgreen",
      "cadetblue",
      "darkpurple",
      "white",
      "pink",
      "lightblue",
      "lightgreen",
      "gray",
      "black",
      "lightgray",
  ]

  if isinstance(data, pd.DataFrame):
    df = data
  elif not data.startswith("http") and (not os.path.exists(data)):
    raise FileNotFoundError("The specified input csv does not exist.")
  else:
    df = pd.read_csv(data)

  col_names = df.columns.values.tolist()

  if color_column is not None and color_column not in col_names:
    raise ValueError(
        f"The color column {color_column} does not exist in the dataframe."
    )

  if color_column is not None:
    items = list(set(df[color_column]))
  else:
    items = None

  if color_column is not None and marker_colors is None:
    if len(items) > len(color_options):
      raise ValueError(
          f"The number of unique values in the color column {color_column} is greater than the number of available colors."
      )
    else:
      marker_colors = color_options[: len(items)]
  elif color_column is not None and marker_colors is not None:
    if len(items) != len(marker_colors):
      raise ValueError(
          f"The number of unique values in the color column {color_column} is not equal to the number of available colors."
      )

  if items is not None:
    if len(icon_colors) == 1:
      icon_colors = icon_colors * len(items)
    elif len(items) != len(icon_colors):
      raise ValueError(
          f"The number of unique values in the color column {color_column} is not equal to the number of available colors."
      )

    if len(icon_names) == 1:
      icon_names = icon_names * len(items)
    elif len(items) != len(icon_names):
      raise ValueError(
          f"The number of unique values in the color column {color_column} is not equal to the number of available colors."
      )

  if popup is None:
    popup = col_names

  if x not in col_names:
    raise ValueError(
        f"x must be one of the following: {', '.join(col_names)}")

  if y not in col_names:
    raise ValueError(
        f"y must be one of the following: {', '.join(col_names)}")

  # .add_to(self)
  marker_cluster = plugins.MarkerCluster(name=layer_name, **kwargs)

  for idx, row in df.iterrows():
    html = ""
    for p in popup:
      html = html + "<b>" + p + "</b>" + ": " + str(row[p]) + "<br>"
    popup_html = folium.Popup(
        html, min_width=min_width, max_width=max_width)

    if items is not None:
      index = items.index(row[color_column])
      marker_icon = folium.Icon(
          color=marker_colors[index],
          icon_color=icon_colors[index],
          icon=icon_names[index],
          angle=angle,
          prefix=prefix,
      )
    else:
      marker_icon = None

    folium.Marker(
        location=[row[y], row[x]],
        popup=popup_html, 
        tooltip=row["name"],
        icon=marker_icon,
    ).add_to(marker_cluster)

  # if items is not None and add_legend:
  #     marker_colors = [check_color(c) for c in marker_colors]
  #     self.add_legend(
  #         title=color_column.title(), colors=marker_colors, labels=items
  #     )
  return marker_cluster



## 一些常用的点

loc_cug_new = [30.46001618003947, 114.61223316513498]
loc_cug_old = [30.52201873299567, 114.39688111832672]

# fg, points_met = add_FeatureGroup()
cug_new = add_Marker(loc_cug_new, "cug_new")
cug_old = add_Marker(loc_cug_old, "cug_old")
