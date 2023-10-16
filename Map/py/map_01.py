import ipyleaflet as L
from ipyleaflet import *
from htmltools import css
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, reactive_read, register_widget

app_ui = ui.page_fluid(
    ui.div(
        ui.input_slider("zoom", "Map zoom level", value=12, min=1, max=18),
        ui.output_ui("map_bounds"),
        style=css(
            display="flex", justify_content="center", align_items="center", gap="2rem"
        ),
    ),
    output_widget("map"),
)

# m = Map(center=(capitol_loc), zoom=14)
capitol_loc = (38.89, -77.02) #(lat, long)
locations = [(38.89, -77.02), (38.88, -77.02), (38.88, -77.01), (38.873, -77.02), (38.891, -77.02), (38.89, -77.022)]

def create_button_click(event, type, coordinates):
    # def button_click():
    print(event, type, coordinates)
    # return button_click
# def button_click(sample_id):
#     print(str(sample_id))


def add_markers(m):
    for i in range(len(locations)):
        new_marker_loc = (locations[i][0], locations[i][1])
        new_marker = Marker(location=new_marker_loc, draggable=False)
        
        # sample_id = "Sample Id: 1234567"
        new_marker.on_click(create_button_click)
        # new_marker.on_click(button_click(sample_id)) 
        m.add_layer(new_marker)  
    # return m
  

def server(input, output, session):
    # Initialize and display when the session starts (1)
    map = L.Map(center=(capitol_loc), zoom=14) 
    # map = L.Map(center=(51.476852, -0.000500), zoom=12, scroll_wheel_zoom=True)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    add_markers(map)

    register_widget("map", map)

    # When the slider changes, update the map's zoom attribute (2)
    @reactive.Effect
    def _():
        map.zoom = input.zoom()

    # When zooming directly on the map, update the slider's value (2 and 3)
    @reactive.Effect
    def _():
        ui.update_slider("zoom", value=reactive_read(map, "zoom"))

    # Everytime the map's bounds change, update the output message (3)
    @output
    @render.ui
    def map_bounds():
        # print(map)
        center = reactive_read(map, "center")

        if len(center) == 0:
            return

        lat = round(center[0], 4)
        lon = (center[1] + 180) % 360 - 180
        lon = round(lon, 4)

        return ui.p(f"Latitude: {lat}", ui.br(), f"Longitude: {lon}")


app = App(app_ui, server)
