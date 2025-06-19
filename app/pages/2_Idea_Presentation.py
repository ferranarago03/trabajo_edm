# pages/2_Idea_Presentation.py
import streamlit as st
import os
from streamlit_option_menu import option_menu

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Presentación de la Idea",
    page_icon="💡",
    layout="centered",  # Puedes usar "wide" si prefieres más espacio
)

# --- Estilos del Menú (misma que Home.py) ---
menu_styles = {
    "container": {
        "padding": "0!important",
        "background-color": "white",
        "border-bottom": "1px solid #E0E0E0",
        "margin-bottom": "2.5rem",
        "box-shadow": "0 2px 4px rgba(0,0,0,0.03)",
    },
    "icon": {"color": "white", "font-size": "1.1rem", "vertical-align": "middle"},
    "nav-link": {
        "font-size": "1rem",
        "font-weight": "500",
        "text-align": "center",
        "margin": "0px 8px",
        "padding": "18px 15px",
        "--hover-color": "#e7f3ff",
        "color": "#333333",
        "border-bottom": "3px solid transparent",
    },
    "nav-link-selected": {
        "background-color": "#002D62",
        "color": "white",
        "font-weight": "600",
        "border-bottom": "3px solid #FF7F0E",
        "border-radius": "6px 6px 0 0",
        "padding-bottom": "15px",
    },
}

# --- Mapeo de nombres de display a rutas de archivo ---
page_map = {
    "Página Principal": "home.py",
    "Planificador de Rutas": "pages/1_Implementation.py",
    "Presentación de la Idea": "pages/2_Idea_Presentation.py",
}

# --- Lógica para determinar la página actual y el índice por defecto del menú ---
current_page_filename = os.path.basename(__file__)  # "2_Idea_Presentation.py"
current_page_full_path = f"pages/{current_page_filename}"

# Encontrar el nombre de display de la página actual
current_display_name = None
for display_name, file_path in page_map.items():
    if file_path == current_page_full_path:
        current_display_name = display_name
        break

# Establecer índice por defecto para el menú
default_index_for_menu = 0
if current_display_name:
    default_index_for_menu = list(page_map.keys()).index(current_display_name)

# --- Menú de Navegación ---
seleccion = option_menu(
    menu_title=None,
    options=list(page_map.keys()),
    icons=["house-door-fill", "map", "lightbulb-fill"],
    menu_icon="list-ul",
    orientation="horizontal",
    default_index=default_index_for_menu,
    styles=menu_styles,
    key="main_navigation_menu_presentation",
)

# --- Manejo de la navegación ---
target_file_path = page_map[seleccion]

# Solo redirigir si es diferente a la página actual
if target_file_path != current_page_full_path:
    # Actualizar el estado de sesión si existe
    if "current_page_for_nav" in st.session_state:
        st.session_state.current_page_for_nav = seleccion

    # Redirigir a la página seleccionada
    st.switch_page(target_file_path)

# --- Contenido Principal de "Presentación de la Idea" ---
st.title("💡 Presentación de la Idea: Movilidad Urbana Inteligente en Valencia")

st.markdown("""
---
### Visión del Proyecto
Nuestro proyecto tiene como objetivo mejorar la movilidad urbana en Valencia mediante una aplicación intuitiva y eficiente de planificación de rutas.
Nos centramos en métodos de transporte sostenibles, promoviendo caminar y el uso de la bicicleta como modos principales de desplazamiento.

### Características Clave
* **Planificación Multimodal de Rutas**: Los usuarios pueden elegir entre rutas a pie, en bicicleta personal o con ValenBisi.
* **Interfaz de Mapa Interactiva**: Selección fácil de puntos de inicio y destino directamente en un mapa interactivo con Folium.
* **Rutas Optimizadas**: Utiliza datos de OpenStreetMap y `osmnx` para encontrar rutas inteligentes según la red vial y el modo de transporte elegido.
* **Experiencia Amigable**: Una interfaz simple y limpia, diseñada para todo tipo de usuarios.

### Público Objetivo
Esta aplicación está pensada para:
* **Residentes de Valencia**: Personas que se desplazan diariamente y buscan opciones de transporte eficientes y sostenibles.
* **Turistas**: Visitantes que desean explorar Valencia a pie o en bicicleta.
* **Urbanistas**: Para analizar rutas populares e identificar áreas de mejora en la infraestructura.

### Tecnologías Utilizadas
* **Streamlit**: Para crear la aplicación web interactiva.
* **Folium**: Para visualizar datos geográficos y mapas interactivos.
* **OSMnx**: Para descargar, construir, analizar y visualizar redes de calles desde OpenStreetMap.
* **Python**: El lenguaje de programación principal.

### Mejoras Futuras
* **Tráfico / Disponibilidad en Tiempo Real**: Integrar datos en vivo sobre la disponibilidad de estaciones ValenBisi o el estado del tráfico.
* **Opciones de Accesibilidad**: Considerar rutas optimizadas para personas con movilidad reducida.
* **Personalización de Rutas**: Permitir que los usuarios especifiquen preferencias como "evitar cuestas" o "ruta más escénica".
* **Tiempo y Distancia Estimada**: Mostrar el tiempo de viaje y la distancia calculados para la ruta generada.
* **Integración con Transporte Público**: Combinar rutas a pie o en bicicleta con opciones de transporte público.

---
""")
