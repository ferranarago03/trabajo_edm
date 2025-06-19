# pages/2_Idea_Presentation.py
import streamlit as st
from nav import show_nav_menu
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(
    page_title="Presentación de la Idea",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    st.session_state.current_page_for_nav = "Presentación de la Idea"

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

# --- Contenido Principal ---
st.header("Presentación de la Idea: Movilidad Urbana Inteligente en Valencia")

st.markdown("""
### Visión del Proyecto
El proyecto tiene como objetivo mejorar la movilidad urbana, proporcionando opciones de rutas inteligentes, sostenibles y seguras. Está enfocado en promover métodos de transporte respetuosos con el entorno dentro de la ciudad y de promover rutas con gran cantidad de sombra y mostrar fuentes públicas donde hidratarse durante el trayecto para luchar contra las altas temperaturas que genera el cambio climático.

### Características Clave
* **Obtención de los datos**: 
    * Descarga de datos de OpenStreetMap (OSM) para Valencia. Obtención de los dos grafo utilizados para el cálculo de las rutas.
    * Descarga de datos abiertos de la ciudad de Valencia a través de la API de Open Data. De esta forma se han obtenido todas las fuentes públicas de la ciudad así como los árboles que hay en la ciudad para calcular las zonas con sombra.
            
        También se hace uso de este portal para obtener los datos de las estaciones de ValenBisi y poder saber cuáles de ellas son las más cercanas y tienen bicicletas y plazas disponibles. Este es un valor relativamente actual ya que se descarga en el momento de hacer la consulta y en la API se actualiza cada 15 minutos.
    * Descarga de los datos de temperatura a través de la API de Open Meteo. Estos datos se actualizan cada hora y permiten calcular la temperatura actual en Valencia para poder calcular el número de paradas que se deben hacer en las fuentes públicas y la importacia de la sombra en la ruta.
* **Cálculo de los pesos por la sombra**: Para calcular la importancia de la sombra, se ha usado el dataset con los árboles de Valencia, junto con las proyecciones de los grafos. Para cada tramo del grafo (es decir, una arista entre dos nodos), se construye una zona de influencia de 15 metros alrededor del tramo. Dre esa manea, con un índice espacial, se consultan de manera eficiente todos los árboles situados dentro de la zona, ya que cuantos más árboles, más sombra. Para calcular los pesos del grafo, se definen distintos rangos de temperatura, de 5 en 5 grados y de 0 Cº a 40 Cº.  Para cada diferente rango, se establecen diferentes pesos dependiendo de la importancia de la longitud o del número de árboles. A mayor temperatura, se le dará un poco más de importancia ir por una zona sombreada, sin embargo, a menor temperatura, se le dará más importancia a la longitud. La fórmula utilizada final es: (importancia_longitud * longitud) - (importancia_sombra*número de arboles) + 1000 (esta suma final se añade para garantizar que se den pesos positivos para no tener problemas con el algoritmo Dijkstra).
* **Cálculo de la ruta**:
    1. El primer paso consiste en obtener los nodos del grafo correspondiente que más cerca se encuentren del punto de inicio y del punto de destino, ya que se desea que la selección de estos puntos sea interactiva.
    2. A continuación, se calcula la ruta más corta entre estos dos nodos.
    3. En el caso de la ruta en bicicleta, además de calcular la ruta más corta considerando solo la calles con carril bici, se calcula la ruta caminando para llegar del punto de inicio al carril bici más cercano y del carril bici más cercano al punto de destino.
    4. Finalmente, para el ValenBisi, se realiza un proceso similar al de la bicicleta, pero se guía en primer lugar a la estación de ValenBisi más cercana al punto de inicio y a la incorporación al carril bici, y al final se guía a la estación de ValenBisi más cercana al punto de destino. Ambas estaciones se seleccionan considerando la disponibilidad de bicicletas y plazas en el momento de la consulta.
* **Obtención de las fuentes públicas**: Una vez calculada la ruta y su distancia total, se procede a obtener las fuentes públicas que se encuentran a lo largo de la ruta. Para ello, se calcula el número de paradas que se aconsejaría realizar en función de la temperatura actual de Valencia y, con ello, la distancia que se debe recorrer entre cada parada. A partir de este valor, se va recorriendo la ruta y buscando, en la distancia correcta, las fuentes públicas que se encuentren cerca de la ruta calculada.
* **Visualización de los resultados**: Por último, se visulizan todos los resultados en un mapa interactivo realizado con Folium y presentado en la aplicación web con Streamlit. En este mapa se muestran las rutas calculadas y las fuentes públicas, así como la temperatura actual de Valencia, la distancia de la ruta o el número de paradas recomendadas.

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

""")
