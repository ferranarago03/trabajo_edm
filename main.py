import streamlit as st
from streamlit_folium import st_folium
import folium
import sys
import osmnx as ox
from shapely.geometry import shape
import pandas as pd

sys.path.append("./src/")

from utils import get_valencian_open_data, get_gdf

from fuentes import get_nearest_water_fountains_on_route, print_fountains

from routes import get_route, print_route, get_valenbisi_route, print_stations


graph_cycling = ox.load_graphml("data/valencia_cycling_network.graphml")
graph_walking = ox.load_graphml("data/valencia_walking_network.graphml")
public_fountains = pd.read_csv("data/fonts_publiques.csv")
public_fountains["geometry"] = public_fountains["geo_shape"].apply(
    lambda x: shape(eval(x))
)
public_fountains_gdf = get_gdf(public_fountains)

temp = 20


st.title("Define inicio y fin de tu ruta")

# 1. Control para elegir qué punto vamos a fijar
st.sidebar.header("Tipo de ruta")
# Selectbox to choose the type of route
tipo_opciones = [
    "Caminando",
    "En bicicleta",
    "Valenbisi",
]  # Opciones para el tipo de ruta
type_route = st.sidebar.selectbox("¿Qué tipo de ruta quieres definir?", tipo_opciones)

st.sidebar.header("Selecciona el punto de la ruta")
# Radio button to choose between start and end point
# (This could also be a selectbox or a dropdown)


punto_opciones = ["Inicio", "Fin"]  # Opciones para el punto

punto = st.sidebar.radio("¿Qué punto quieres fijar?", punto_opciones)

# 2. Inicializa en sesión las coordenadas si no existen
if "start" not in st.session_state:
    st.session_state.start = None
if "end" not in st.session_state:
    st.session_state.end = None

# 3. Crea el mapa; opcionalmente centra en el último punto conocido
centro = [39.4699, -0.3763]
if st.session_state.start:
    centro = [st.session_state.start["lat"], st.session_state.start["lng"]]
elif st.session_state.end:
    centro = [st.session_state.end["lat"], st.session_state.end["lng"]]

m = folium.Map(location=centro, zoom_start=15)

# 4. Añade los marcadores ya guardados
if st.session_state.start:
    folium.Marker(
        [st.session_state.start["lat"], st.session_state.start["lng"]],
        popup="Inicio",
        icon=folium.Icon(color="green"),
    ).add_to(m)
if st.session_state.end:
    folium.Marker(
        [st.session_state.end["lat"], st.session_state.end["lng"]],
        popup="Fin",
        icon=folium.Icon(color="red"),
    ).add_to(m)

# 5. Si ya tenemos ambos puntos, dibuja la ruta (línea)
if st.session_state.start and st.session_state.end:
    if type_route == "Caminando":
        route, dist = get_route(
            (st.session_state.start["lat"], st.session_state.start["lng"]),
            (st.session_state.end["lat"], st.session_state.end["lng"]),
            graph_walking,
        )

        print_route(route, graph_walking, m, color="blue")

        fountains_on_route = get_nearest_water_fountains_on_route(
            graph_walking,
            dist,
            route,
            "Caminando",
            temp,
            public_fountains_gdf,
        )

        print_fountains(fountains_on_route, public_fountains_gdf, m)

    if type_route == "En bicicleta":
        route, dist = get_route(
            (st.session_state.start["lat"], st.session_state.start["lng"]),
            (st.session_state.end["lat"], st.session_state.end["lng"]),
            graph_cycling,
        )

        print_route(route, graph_cycling, m, color="blue")

        fountains_on_route = get_nearest_water_fountains_on_route(
            graph_cycling,
            dist,
            route,
            "En bicicleta",
            temp,
            public_fountains_gdf,
        )

        print_fountains(fountains_on_route, public_fountains_gdf, m)

    if type_route == "Valenbisi":
        params = {
            "rows": 100,
        }
        url = "https://valencia.opendatasoft.com//api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"
        valenbisi_stations = get_valencian_open_data(url, params)

        valenbisi_stations["geometry"] = valenbisi_stations["geo_shape"].apply(shape)
        valenbisi_stations = get_gdf(valenbisi_stations)
        valenbisi_stations = valenbisi_stations[valenbisi_stations["open"] == "T"]

        (
            ini_walking_route,
            dist_ini,
            cycling_route,
            dist_cycling,
            end_walking_route,
            dist_end,
            ini_station,
            end_station,
            dist,
        ) = get_valenbisi_route(
            (st.session_state.start["lon"], st.session_state.start["lat"]),
            (st.session_state.end["lon"], st.session_state.end["lat"]),
            graph_cycling,
            graph_walking,
            valenbisi_stations,
        )

        print_stations(ini_station, end_station, m)
        print_route(ini_walking_route, graph_walking, m, color="green")
        print_route(cycling_route, graph_cycling, m, color="blue")
        print_route(end_walking_route, graph_walking, m, color="green")

        fountains_ini = get_nearest_water_fountains_on_route(
            graph_walking,
            dist_ini,
            route,
            "Caminando",
            temp,
            public_fountains_gdf,
        )

        fountains_cycling = get_nearest_water_fountains_on_route(
            graph_cycling,
            dist_cycling,
            route,
            "En bicicleta",
            temp,
            public_fountains_gdf,
        )

        fountains_end = get_nearest_water_fountains_on_route(
            graph_walking,
            dist_end,
            route,
            "Caminando",
            temp,
            public_fountains_gdf,
        )

        print_fountains(fountains_ini, public_fountains_gdf, m)
        print_fountains(fountains_cycling, public_fountains_gdf, m)
        print_fountains(fountains_end, public_fountains_gdf, m)


# 6. Plugin para capturar clics y colocar un marcador temporal
m.add_child(
    folium.ClickForMarker(
        popup=f"Selecciona el {punto.lower()} de la ruta",
    )
)

# 7. Renderiza el mapa y captura el clic
map_data = st_folium(m, width=700, height=500)

# 8. Si ha habido un clic, guárdalo según la elección del usuario
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]
    if punto == "Inicio":
        st.session_state.start = {"lat": lat, "lng": lng}
        st.success(f"Punto de **inicio** guardado en {lat:.6f}, {lng:.6f}")
    else:
        st.session_state.end = {"lat": lat, "lng": lng}
        st.success(f"Punto de **fin** guardado en {lat:.6f}, {lng:.6f}")

    # Para que el mapa se refresque con los nuevos marcadores/linea:
    st.rerun()
