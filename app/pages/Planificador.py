import streamlit as st
from streamlit_folium import st_folium
import folium
from branca.element import Template, MacroElement
from shapely.geometry import shape
import pandas as pd
from datetime import datetime as dt
from zoneinfo import ZoneInfo
import gdown

from pathlib import Path
import os
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

from nav import show_nav_menu

APP_DIR = Path(__file__).resolve().parent.parent

FILE_ID = "1aPsZF__V9mNxLMmcixAF0A8joReIn_FC"
FILENAME = "data/valencia_walking_sombra.graphml"

try:
    st.set_page_config(
        page_title="VALEN FRESC | Planificador de Rutas",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🗺️",
    )
except AttributeError:
    FAVICON_FILENAME = "route_planner.png"
    FAVICON_LOCAL_PATH_OBJ = APP_DIR / FAVICON_FILENAME

    page_icon_to_use = "https://www.esade.edu/favicon.ico"
    if FAVICON_LOCAL_PATH_OBJ.is_file():
        page_icon_to_use = str(FAVICON_LOCAL_PATH_OBJ)

    st.set_page_config(
        page_title="VALEN FRESC | Planificador de Rutas",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🗺️",
    )


st.markdown(
    """
    <style>
      /* Oculta la navegación automática de páginas en el sidebar */
      [data-testid="stSidebarNav"] {
        display: none;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

if "current_page_for_nav" not in st.session_state:
    st.session_state.current_page_for_nav = "Planificador de Rutas"

show_nav_menu(st.session_state.current_page_for_nav)


def load_main_app_css(file_name: str):
    css_path = APP_DIR / file_name
    if css_path.is_file():
        try:
            with open(css_path, encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al cargar CSS desde {css_path}: {e}")
    else:
        st.warning(
            f"Archivo CSS '{file_name}' no encontrado en {css_path}. Asegúrate de que esté en el directorio '{APP_DIR.name}'."
        )


load_main_app_css("styles.css")


# ----------------------
# Functions for loading data and caching
# ----------------------
@st.cache_data
def get_data_from_drive(file_id: str, filename: str):
    """Descarga el fichero de Google Drive si no existe localmente."""
    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, filename, quiet=False)
    return filename


# 1. Cache-loading of heavy static resources
@st.cache_resource
def load_graphs():
    cycling_graph = read_graph("data/valencia_cycling_sombra.graphml")
    walking_graph = read_graph(FILENAME)
    return cycling_graph, walking_graph


@st.cache_data
def load_public_fountains():
    df = pd.read_csv("data/fonts_publiques.csv")
    df["geometry"] = df["geo_shape"].apply(lambda x: shape(eval(x)))
    return get_gdf(df)


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


# ----------------------
# Global variables and initial setup
# ----------------------
get_data_from_drive(FILE_ID, FILENAME)

# Load cached data
graph_cycling, graph_walking = load_graphs()
public_fountains_gdf = load_public_fountains()
now = dt.now(tz=ZoneInfo("UTC"))

if "now" not in st.session_state:
    st.session_state.now = now
    st.session_state.first_run = True

temp = fetch_temperature(now)

range_temp = get_range(temp)

# ----------------------
# Streamlit app layout and logic
# ----------------------
st.header("Intrucciones para el Planificador de Rutas")
st.markdown(
    """
    1. **Selecciona el tipo de ruta**: Puedes elegir entre **Caminando**, **En Bicicleta** o **Valenbisi**.
    2. **Define los puntos de inicio y fin**:
        * Selecciona en el menú de la izquierda si deseas intruducir el inicio o la llegada de tu ruta.
        * Una vez seleccionado, haz clic en el mapa para fijar el punto deseado.
        * Cambia a la opción contraria para fijar el otro punto.
    3. **Visualiza la ruta**: Una vez que hayas fijado ambos puntos, el mapa mostrará la ruta calculada.
    4. **Consulta las fuentes de agua**: Se mostrarán las fuentes de agua cercanas a tu ruta, teniendo en cuenta la temperatura actual de Valencia. Podrás acceder a su información haciendo clic en los iconos de las fuentes en el mapa.
    5. **Consulta las estaciones de ValenBisi**: Si has seleccionado la opción de ValenBisi, se mostrarán las estaciones disponibles en tu ruta, indicando, el número de bicicletas disponibles para la estción de inicio y el número de plazas disponibles para la de llegada.
        Estas siempre tendrán alguna bicicleta disponible y alguna plaza libre, ya que el sistema se encarga de que así sea.
    """
)

st.header("Planificador")
st.markdown("")

# Sidebar inputs
with st.sidebar:
    st.header("Tipo de ruta")
    tipo_opciones = ["Caminando", "Bicicleta", "Valenbisi"]
    type_route = st.selectbox("¿Qué tipo de ruta quieres definir?", tipo_opciones)

    st.header("Selecciona el punto de la ruta")
    punto_opciones = ["Inicio", "Fin"]
    punto = st.radio("¿Qué punto quieres fijar?", punto_opciones)

    st.markdown("---")
    st.markdown("#### Autores")
    st.markdown(
        """
        - Ferran Aragó Ausina
        - Carles Navarro Esteve  
        - Aleixandre Tarrasó Sorní
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption(f"© {pd.Timestamp.now().year} Planificador de Rutas | v1.0")
    st.caption("Movilidad Urbana Sostenible")
    st.markdown("---")

# Session state for start/end
if "start" not in st.session_state:
    st.session_state.start = None
if "end" not in st.session_state:
    st.session_state.end = None

# Center map on last known point
centro = [39.4699, -0.3763]
if st.session_state.start and st.session_state.end:
    centro = [
        (st.session_state.start["lat"] + st.session_state.end["lat"]) / 2,
        (st.session_state.start["lng"] + st.session_state.end["lng"]) / 2,
    ]
elif st.session_state.start:
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

dist_total = 0
okey = True
paradas_total = 0
fuentes_total = 0
if st.session_state.start and st.session_state.end:
    start_coord = (st.session_state.start["lat"], st.session_state.start["lng"])
    end_coord = (st.session_state.end["lat"], st.session_state.end["lng"])

    if type_route == "Caminando":
        route, dist = compute_route(start_coord, end_coord, graph_walking, range_temp)
        print_route(route, graph_walking, m, color="green")

        fountains_on_route, paradas = compute_fountains(
            graph_walking, dist, route, type_route, temp, public_fountains_gdf
        )
        print_fountains(fountains_on_route, public_fountains_gdf, m)

        paradas_total += paradas
        fuentes_total += len(fountains_on_route)
        dist_total = dist

    elif type_route == "Bicicleta":
        ini_walk, dist_ini, cycle, dist_cycle, end_walk, dist_end = (
            compute_cycling_route(
                start_coord, end_coord, graph_cycling, graph_walking, range_temp
            )
        )

        if ini_walk and cycle and end_walk:
            print_route(ini_walk, graph_walking, m, color="green")
            print_route(cycle, graph_cycling, m, color="blue")
            print_route(end_walk, graph_walking, m, color="green")
        else:
            okey = False
            st.error(
                "No se ha podido calcular la ruta en bicicleta entre los puntos seleccionados."
            )
            st.stop()

        for seg_graph, seg_dist, seg_route, seg_mode in [
            (graph_walking, dist_ini, ini_walk, "Caminando"),
            (graph_cycling, dist_cycle, cycle, "En Bicicleta"),
            (graph_walking, dist_end, end_walk, "Caminando"),
        ]:
            fountains_on_segment, paradas = compute_fountains(
                seg_graph,
                seg_dist,
                seg_route,
                seg_mode,
                temp,
                public_fountains_gdf,
            )
            print_fountains(fountains_on_segment, public_fountains_gdf, m)
            paradas_total += paradas
            fuentes_total += len(fountains_on_segment)

        dist_total = dist_ini + dist_cycle + dist_end

    elif type_route == "Valenbisi":
        # Fetch station data once

        if st.session_state.first_run or now - st.session_state.now > pd.Timedelta(
            minutes=10
        ):
            st.session_state.now = now
            st.session_state.first_run = False
            params = {"rows": 100}
            url = (
                "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/"
                "datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"
            )
            st.session_state.valenbisi_stations = fetch_valenbisi_stations(url, params)

        try:
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
                st.session_state.valenbisi_stations,
                range_temp,
            )

            print_stations(ini_station, end_station, m)
            print_route(ini_walk, graph_walking, m, color="green")
            print_route(cycle, graph_cycling, m, color="blue")
            print_route(end_walk, graph_walking, m, color="green")

        except IndexError:
            okey = False
            st.error(
                "No se ha podido calcular la ruta en ValenBisi entre los puntos seleccionados."
            )
            st.stop()

        for seg_graph, seg_dist, seg_route, seg_mode in [
            (graph_walking, dist_ini, ini_walk, "Caminando"),
            (graph_cycling, dist_cycle, cycle, "En Bicicleta"),
            (graph_walking, dist_end, end_walk, "Caminando"),
        ]:
            fts, paradas = compute_fountains(
                seg_graph, seg_dist, seg_route, seg_mode, temp, public_fountains_gdf
            )
            print_fountains(fts, public_fountains_gdf, m)
            paradas_total += paradas
            fuentes_total += len(fts)

        dist_total = dist_ini + dist_cycle + dist_end

    legend_html = """
    {% macro html(this, kwargs) %}
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 140px;
        height: 70px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        ">
        &nbsp;<b>Leyenda</b><br>
        &nbsp;<i style="background:green;
                    display:inline-block;
                    width:12px;
                    height:12px;
                    margin-right:6px;"></i> Caminando<br>
        &nbsp;<i style="background:blue;
                    display:inline-block;
                    width:12px;
                    height:12px;
                    margin-right:6px;"></i> Bicicleta
    </div>
    {% endmacro %}
    """
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

if okey and dist_total > 0:
    st.markdown(
        f"La distancia total de la ruta es de **{dist_total:.2f} metros**.\nHace una temperatura de **{temp:.2f}°C** en Valencia, por lo que se recomienda hacer un total de **{paradas_total} paradas**, pero se han encontrado un total de **{fuentes_total} fuentes** cercanas a la ruta."
    )


# 3. Add click handler
m.add_child(folium.ClickForMarker(popup=f"Selecciona el {punto.lower()} de la ruta"))
map_data = st_folium(m, width=1500, height=700)

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
