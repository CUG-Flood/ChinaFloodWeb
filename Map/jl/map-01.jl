using JSServe
using Leaflet

# 创建一个简单的Leaflet地图
m = leaflet()

# 设置地图的中心和缩放级别
setView(m, [0, 0], 2)

# 添加一个标记点
marker = marker([0, 0])
addMarker(m, marker)

# 创建JavaScript回调函数以处理点击事件
@js function handleMapClick(e)
    alert("Clicked at: " * string(e.latlng.lat) * ", " * string(e.latlng.lng))
end

# 将点击事件监听器添加到地图
add_event_listener(marker, "click", handleMapClick)

# 创建一个示例页面并启动JSServe服务器
page = Page("Interactive Map Example", m)
display(page, init=true)
