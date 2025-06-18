import streamlit as st
from streamlit_folium import st_folium
import folium
from shapely.geometry import shape
import pandas as pd
from datetime import datetime as dt
from zoneinfo import ZoneInfo

# Import your existing utilities without modifying their internal logic
import sys

sys.path.append("./src/")
from utils import get_valencian_open_data, get_gdf, read_graph
from fountains import get_nearest_water_fountains_on_route, print_fountains
from routes import (
    get_route,
    print_route,
    get_valenbisi_route,
    get_cycling_route,
    print_stations,
)
from temperature import get_temperature_data


# 1. Cache-loading of heavy static resources
@st.cache_resource
def load_graphs():
    cycling_graph = read_graph("data/valencia_cycling_sombra.graphml")
    walking_graph = read_graph("data/valencia_walking_sombra.graphml")
    now = dt.now(tz=ZoneInfo("UTC"))
    return cycling_graph, walking_graph, now


@st.cache_data
def load_public_fountains():
    df = pd.read_csv("data/fonts_publiques.csv")
    df["geometry"] = df["geo_shape"].apply(lambda x: shape(eval(x)))
    return get_gdf(df)


@st.cache_data
def fetch_valenbisi_stations(url, params):
    df = get_valencian_open_data(url, params)
    df["geometry"] = df["geo_shape"].apply(shape)
    gdf = get_gdf(df)
    return gdf[gdf["open"] == "T"]


# Cache the route computation by inputs
@st.cache_data
def compute_route(s, e, _graph, range_temp="length"):
    return get_route(s, e, _graph, range_temp)


@st.cache_data
def compute_valenbisi_trip(
    start, end, _cycling_graph, _walking_graph, _stations, range_temp="length"
):
    return get_valenbisi_route(
        start,
        end,
        _cycling_graph,
        _walking_graph,
        _stations,
        range_temp,
    )


# Cache fountains lookup, mark graph param as unhashable
@st.cache_data
def compute_fountains(_g, d, r, mode, temp_val, _fountains_gdf):
    return get_nearest_water_fountains_on_route(
        _g, d, r, mode, temp_val, _fountains_gdf
    )


@st.cache_data
def compute_cycling_route(
    start, end, _cycling_graph, _walking_graph, range_temp="length"
):
    return get_cycling_route(start, end, _cycling_graph, _walking_graph, range_temp)


@st.cache_data
def fetch_temperature(now):
    return get_temperature_data(now)


@st.cache_data
def get_range(temp):
    for i in range(0, 41, 5):
        if temp - 5 < i:
            return f"peso_{i}_{i + 5}"


# Load cached data
graph_cycling, graph_walking, now = load_graphs()
public_fountains_gdf = load_public_fountains()

temp = fetch_temperature(now)

range_temp = get_range(temp)

st.title("Define inicio y fin de tu ruta")

# Sidebar inputs
st.sidebar.header("Tipo de ruta")
tipo_opciones = ["Caminando", "En Bicicleta", "Valenbisi"]
type_route = st.sidebar.selectbox("¿Qué tipo de ruta quieres definir?", tipo_opciones)

st.sidebar.header("Selecciona el punto de la ruta")
punto_opciones = ["Inicio", "Fin"]
punto = st.sidebar.radio("¿Qué punto quieres fijar?", punto_opciones)

# Session state for start/end
if "start" not in st.session_state:
    st.session_state.start = None
if "end" not in st.session_state:
    st.session_state.end = None

# Center map on last known point
centro = [39.4699, -0.3763]
if st.session_state.start:
    centro = [st.session_state.start["lat"], st.session_state.start["lng"]]
elif st.session_state.end:
    centro = [st.session_state.end["lat"], st.session_state.end["lng"]]

m = folium.Map(location=centro, zoom_start=15)

# Add existing markers
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

# 2. Compute and draw route only if both points are set
if st.session_state.start and st.session_state.end:
    start_coord = (st.session_state.start["lat"], st.session_state.start["lng"])
    end_coord = (st.session_state.end["lat"], st.session_state.end["lng"])

    if type_route == "Caminando":
        route, dist = compute_route(start_coord, end_coord, graph_walking, range_temp)
        print_route(route, graph_walking, m, color="green")

        fountains_on_route = compute_fountains(
            graph_walking, dist, route, type_route, temp, public_fountains_gdf
        )
        print_fountains(fountains_on_route, public_fountains_gdf, m)

    elif type_route == "En Bicicleta":
        ini_walk, dist_ini, cycle, dist_cycle, end_walk, dist_end = (
            compute_cycling_route(
                start_coord, end_coord, graph_cycling, graph_walking, range_temp
            )
        )

        print_route(ini_walk, graph_walking, m, color="green")
        print_route(cycle, graph_cycling, m, color="blue")
        print_route(end_walk, graph_walking, m, color="green")

        # Fountains for each segment
        for seg_graph, seg_dist, seg_route, seg_mode in [
            (graph_walking, dist_ini, ini_walk, "Caminando"),
            (graph_cycling, dist_cycle, cycle, "En Bicicleta"),
            (graph_walking, dist_end, end_walk, "Caminando"),
        ]:
            fountains_on_segment = compute_fountains(
                seg_graph,
                seg_dist,
                seg_route,
                seg_mode,
                temp,
                public_fountains_gdf,
            )
            print_fountains(fountains_on_segment, public_fountains_gdf, m)

    elif type_route == "Valenbisi":
        # Fetch station data once
        params = {"rows": 100}
        url = (
            "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/"
            "datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"
        )
        valenbisi_stations = fetch_valenbisi_stations(url, params)

        (
            ini_walk,
            dist_ini,
            cycle,
            dist_cycle,
            end_walk,
            dist_end,
            ini_station,
            end_station,
        ) = compute_valenbisi_trip(
            start_coord,
            end_coord,
            graph_cycling,
            graph_walking,
            valenbisi_stations,
            range_temp,
        )

        print_stations(ini_station, end_station, m)
        print_route(ini_walk, graph_walking, m, color="green")
        print_route(cycle, graph_cycling, m, color="blue")
        print_route(end_walk, graph_walking, m, color="green")

        # Fountains for each segment
        for seg_graph, seg_dist, seg_route, seg_mode in [
            (graph_walking, dist_ini, ini_walk, "Caminando"),
            (graph_cycling, dist_cycle, cycle, "En Bicicleta"),
            (graph_walking, dist_end, end_walk, "Caminando"),
        ]:
            fts = compute_fountains(
                seg_graph, seg_dist, seg_route, seg_mode, temp, public_fountains_gdf
            )
            print_fountains(fts, public_fountains_gdf, m)

# 3. Add click handler
m.add_child(folium.ClickForMarker(popup=f"Selecciona el {punto.lower()} de la ruta"))
map_data = st_folium(m, width=700, height=500)

# 4. Handle new click
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]
    if punto == "Inicio":
        st.session_state.start = {"lat": lat, "lng": lng}
        st.success(f"Punto de **inicio** guardado en {lat:.6f}, {lng:.6f}")
    else:
        st.session_state.end = {"lat": lat, "lng": lng}
        st.success(f"Punto de **fin** guardado en {lat:.6f}, {lng:.6f}")

    # Trigger a rerun so cached functions will be used for recompute
    st.rerun()
