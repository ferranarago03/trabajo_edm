import streamlit as st
from streamlit_folium import st_folium
import folium
import sys
import osmnx as ox

sys.path.append("./src/")

from utils import get_route

st.title("Define inicio y fin de tu ruta")

# 1. Control para elegir qué punto vamos a fijar
st.sidebar.header("Tipo de ruta")
# Selectbox to choose the type of route
tipo_opciones = ["Caminando", "En bicicleta"]  # Opciones para el tipo de ruta
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
    graph_cycling = ox.load_graphml("data/valencia_cycling_network.graphml")
    graph_walking = ox.load_graphml("data/valencia_walking_network.graphml")

    if type_route == "Caminando":
        route = get_route(
            (st.session_state.start["lat"], st.session_state.start["lng"]),
            (st.session_state.end["lat"], st.session_state.end["lng"]),
            graph_walking,
        )

        folium.PolyLine(
            locations=[
                [graph_walking.nodes[node]["y"], graph_walking.nodes[node]["x"]]
                for node in route
            ],
            color="blue",
            weight=5,
            opacity=0.7,
        ).add_to(m)

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
