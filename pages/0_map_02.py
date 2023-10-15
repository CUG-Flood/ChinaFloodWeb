import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium, folium_static


# 创建一个Folium地图
m = folium.Map(location=[51.5, -0.09], zoom_start=10)
# 创建一个MarkerCluster用于添加标记
marker_cluster = MarkerCluster().add_to(m)

# Streamlit界面
st.write("Folium Map Example")

# 在Streamlit中显示地图
# st.write(m)
st_folium(m, returned_objects=[])

# 添加Streamlit按钮来触发事件
if st.button("Get Clicked Coordinates"):
    clicked_coordinates = None

    # 添加一个自定义的JavaScript代码块来处理地图上的单击事件
    html = """
    <script>
    var map = document.querySelector('.folium-map');
    map.addEventListener('click', function(e){
        var lat = e.latlng.lat;
        var lon = e.latlng.lng;
        var message = 'Latitude: ' + lat + '<br>Longitude: ' + lon;
        var popup = L.popup()
            .setLatLng(e.latlng)
            .setContent(message)
            .addTo(map);
        var marker = L.marker(e.latlng).addTo(marker_cluster);
    });
    </script>
    """

    # 显示Folium地图
    folium.Element(html).add_to(m)

    st.write("Click on the map to get the coordinates")

    # 显示点击的坐标
    st.text(clicked_coordinates)
