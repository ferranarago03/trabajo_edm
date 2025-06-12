import streamlit as st
from streamlit_folium import st_folium
import folium

st.title("Define inicio y fin de tu ruta")

# 1. Control para elegir qué punto vamos a fijar
punto = st.radio("¿Qué punto vas a seleccionar?", ("Inicio", "Fin"))

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

m = folium.Map(location=centro, zoom_start=13)

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
    folium.PolyLine(
        locations=[
            [st.session_state.start["lat"], st.session_state.start["lng"]],
            [st.session_state.end["lat"], st.session_state.end["lng"]],
        ],
        weight=5,
        opacity=0.8,
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
