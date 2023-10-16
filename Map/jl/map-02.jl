using JSServe
JSServe.Page()

leafletjs = JSServe.ES6Module("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js")
leafletcss = JSServe.Asset("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")

struct LeafletMap
  position::NTuple{2,Float64}
  zoom::Int
end

function JSServe.jsrender(session::Session, map::LeafletMap)

  map_div = DOM.div(id="map"; style="height: 700px; width:100%;")

  return JSServe.jsrender(session, DOM.div(
    leafletcss,
    leafletjs,
    map_div,
    js"""
        $(leafletjs).then(L=> {
            const map = L.map('map').setView($(map.position), $(map.zoom));
            L.tileLayer(
                'https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(map);
        })

    """
  ))
end


App() do
  return LeafletMap((51.505, -0.09), 13)
end


App() do
  js = ES6Module("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js")
  css = Asset("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")
  map_div = DOM.div(id="map"; style="height: 300px; width: 100%")
  return DOM.div(
    css, map_div,
    js"""
    $(js).then(L=> {
        const map = L.map('map').setView([51.505, -0.09], 13);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    })
    """
  )
end


using JSServe
app = App() do
  return DOM.div(DOM.h1("hello world"), js"""console.log('hello world')""")
end


App() do
  js = ES6Module("https://esm.sh/v111/leaflet@1.9.3/es2022/leaflet.js")
  css = Asset("https://unpkg.com/leaflet@1.9.3/dist/leaflet.css")
  map_div = DOM.div(id="map"; style="height: 300px; width: 100%")
  return DOM.div(
    css, map_div,
    js"""
    $(js).then(L=> {
        const map = L.map('map').setView([51.505, -0.09], 13);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    })
    """
  )
end


App() do session
  s = Slider(1:3)
  value = map(s.value) do x
    return x^2
  end
  return JSServe.record_states(session, DOM.div(s, value))
end
