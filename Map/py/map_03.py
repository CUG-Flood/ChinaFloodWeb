from shiny import App, render, ui
from shinywidgets import output_widget, reactive_read, register_widget
from ipywidgets import HTML
from ipyleaflet import Map, Marker, Popup

app_ui = ui.page_fluid(
    output_widget("m")
)


def server(input, output, session):
    center = (52.204793, 360.121558)
    m = Map(center=center, zoom=9, close_popup_on_click=False)
    message1 = HTML()
    message1.value = "Try clicking the marker!"

    # Popup with a given location on the map:
    popup = Popup(
        location=center,
        child=message1,
        close_button=False,
        auto_close=False,
        close_on_escape_key=False
    )

    m.add_layer(popup)

    output.m = output_widget("m", width="100%", height="500px")
    register_widget("m", m)

app = App(app_ui, server)
