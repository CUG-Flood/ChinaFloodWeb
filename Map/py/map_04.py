# %%
from ipyleaflet import *

capitol_loc = (38.89, -77.02) #(lat, long)
m = Map(center=(capitol_loc), zoom=14)
locations = [(38.89, -77.02), (38.88, -77.02), (38.88, -77.01), (38.873, -77.02), (38.891, -77.02), (38.89, -77.022)]

def button_click(sample_id):
    print(str(sample_id))


for i in range(len(locations)):
    new_marker_loc = (locations[i][0], locations[i][1])
    new_marker = Marker(location=new_marker_loc, draggable=False)
    
    sample_id = "Sample Id: 1234567"
    
    new_marker.on_click(button_click(sample_id)) 
    m.add_layer(new_marker)
    
m  #Display map

map = L.Map(center=(capitol_loc), zoom=14) 
    # map = L.Map(center=(51.476852, -0.000500), zoom=12, scroll_wheel_zoom=True)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    add_markers(map)
