# Click on circle and get info
library(shiny)
library(leaflet)
library(sf)

ui <- fluidPage(
  leafletOutput("mymap"),
  fluidRow(verbatimTextOutput("map_marker_click"))
)

server <- function(input, output, session) {
  # Create tree geometries
  tree_1g <- st_point(c(-79.2918671415814, 43.6760766531298))
  tree_2g <- st_point(c(-79.4883669334101, 43.6653747165064))
  tree_3g <- st_point(c(-79.2964680812039, 43.7134458013647))

  # Create sfc object with multiple sfg objects
  points_sfc <- st_sfc(tree_1g, tree_2g, tree_3g, crs = 4326)

  # Create tree attributes
  data <- data.frame(
    layerId = c("001", "002", "003"),
    address = c(10, 20, 30),
    street = c("first", "second", "third"),
    tname = c("oak", "elm", "birch"),
    latitude = c(43.6760766531298, 43.6653747165064, 43.7134458013647),
    longitude = c(-79.2918671415814, -79.4883669334101, -79.2964680812039)
  )

  tree_data <- st_sf(data, geometry = points_sfc)

  output$mymap <- renderLeaflet({
    leaflet(data = tree_data) %>%
      addProviderTiles(providers$Stamen.Watercolor) %>%
      # Centre the map in the middle of Toronto
      setView(
        lng = -79.384293,
        lat = 43.685,
        zoom = 11
      ) %>%
      addCircleMarkers(~longitude, ~latitude)
  })

  observeEvent(input$mymap_marker_click, {
    p <- input$mymap_marker_click
    print(str(p))
  })
}

shinyApp(ui, server)
