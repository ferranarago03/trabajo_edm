import streamlit as st
import pandas as pd
from pathlib import Path
import base64
from typing import Union
from nav import show_nav_menu


# --- 0. NO MÁS MÓDULO DE AUTENTICACIÓN ---

# --- Define Paths to Local Assets ---
APP_DIR = Path(__file__).resolve().parent

LOGO_FILENAME = "ValenFresc.png"
LOGO_LOCAL_PATH_OBJ = APP_DIR / LOGO_FILENAME
LOGO_LOCAL_PATH_STR = str(LOGO_LOCAL_PATH_OBJ)

APP_INTRO_FILENAME = "upv.png"
APP_INTRO_LOCAL_PATH_OBJ = APP_DIR / APP_INTRO_FILENAME

# --- 0.1 FAVICON SETUP ---
FAVICON_FILENAME = "route_planner.png"
FAVICON_LOCAL_PATH_OBJ = APP_DIR / FAVICON_FILENAME

page_icon_to_use = "https://www.valenbisi.es/assets/img/logo-contract.png"
if FAVICON_LOCAL_PATH_OBJ.is_file():
    page_icon_to_use = str(FAVICON_LOCAL_PATH_OBJ)
else:
    print(
        f"DEBUG: Local favicon '{FAVICON_FILENAME}' not found at {FAVICON_LOCAL_PATH_OBJ}, using default URL."
    )

# --- 0.2 NO MÁS LOGIN GATEKEEPER ---

if "current_page_for_nav" not in st.session_state:
    st.session_state.current_page_for_nav = "Página Principal"


# --- 1. Page Configuration (FOR THE MAIN APP) ---
st.set_page_config(
    page_title="Aplicación Planificadora de Rutas en Valencia | Bienvenido",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=page_icon_to_use,
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


# --- 2. Load CSS ---
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


# --- Utility Function to Convert Image to Base64 ---
def get_image_as_base64(path_str: str) -> Union[str, None]:
    path_obj = Path(path_str)

    print(f"DEBUG (get_image_as_base64): Buscando imagen en {path_obj}")
    print(f"DEBUG (get_image_as_base64): ¿Existe el archivo? {path_obj.is_file()}")

    if not path_obj.is_file():
        # st.error(f"Image file not found: {path_obj.name}") # Descomentar para error en UI
        return None

    try:
        with open(path_obj, "rb") as image_file:
            print(f"DEBUG (get_image_as_base64): Leyendo imagen {path_obj.name}")
            data = image_file.read()
            encoded_string = base64.b64encode(data).decode()

        ext = path_obj.suffix.lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".gif": "image/gif",
            ".ico": "image/x-icon",
        }
        mime = mime_map.get(ext)
        if not mime:
            print(
                f"DEBUG (get_image_as_base64): Extensión de archivo no soportada: {ext} para {path_obj.name}"
            )
            # st.error(f"Unsupported image format: {ext} for {path_obj.name}") # Descomentar para error en UI
            return None

        return f"data:{mime};base64,{encoded_string}"

    except Exception as e:
        print(
            f"DEBUG (get_image_as_base64): Error al codificar la imagen {path_obj.name} a base64: {e}"
        )
        # st.error(f"Error processing image {path_obj.name}: {e}") # Descomentar para error en UI
        return None


# --- 3. Sidebar Content ---
with st.sidebar:
    sidebar_logo_base64 = get_image_as_base64(LOGO_LOCAL_PATH_STR)
    if sidebar_logo_base64:
        st.markdown(
            f"<img src='{sidebar_logo_base64}' alt='Logotipo de la aplicación' style='display:block; margin:0 auto; width:180px;'>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<h2 style='text-align:center;'>PLANIFICADOR DE RUTAS</h2>",
            unsafe_allow_html=True,
        )

    st.markdown("## Información de Movilidad Urbana")
    st.markdown(
        """
        Tu plataforma de referencia para moverte de forma sostenible y segura por Valencia. Encuentra las rutas más óptimas y frescas de toda la ciudad.
        """
    )
    st.markdown("---")
    st.markdown("#### Navegación Rápida")
    if st.button(
        "🗺️ Planificador de Rutas", use_container_width=True, key="sb_nav_route_planner"
    ):
        st.session_state.current_page_for_nav = "Planificador de Rutas"
        st.switch_page("pages/1_Implementation.py")
    if st.button(
        "💡 Presentación de la Idea",
        use_container_width=True,
        key="sb_nav_idea_presentation",
    ):
        st.session_state.current_page_for_nav = "Presentación de la Idea"
        st.switch_page("pages/2_Idea_Presentation.py")

    st.markdown("---")
    st.markdown("#### Recursos Externos")
    st.markdown(
        "- [OpenStreetMap](https://www.openstreetmap.org/)", unsafe_allow_html=True
    )
    st.markdown(
        "- [Datos abiertos de Valencia](https://valencia.opendatasoft.com/pages/home/)",
        unsafe_allow_html=True,
    )
    st.markdown("#### 👤 Autores")
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


show_nav_menu(st.session_state.current_page_for_nav)


if st.session_state.current_page_for_nav == "Página Principal":
    # --- Hero Section ---
    logo_base64_hero_str = get_image_as_base64(LOGO_LOCAL_PATH_STR)

    hero_section_logo_html = ""
    if logo_base64_hero_str:
        hero_section_logo_html = f"""
        <img src="{logo_base64_hero_str}" alt="Logotipo de la aplicación" style="
            display: block;
            margin: 0 auto 2.5rem auto;
            width: 320px;
            margin-bottom: 2.5rem;
            filter: brightness(1) invert(0);
        ">"""
    else:
        hero_section_logo_html = """<h2 style="color: #fff; font-size:2rem; margin-bottom: 2rem; letter-spacing: 2px; text-transform: uppercase;">PLANIFICADOR DE RUTAS</h2>"""

    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: 5rem 2rem;
            background: linear-gradient(135deg, #00234B 0%, #004080 100%);
            border-radius: 15px;
            margin-bottom: 3.5rem;
            color: blue;
            box-shadow: 0 10px 30px rgba(0, 35, 75, 0.2);
        ">
            {hero_section_logo_html}
            <h1 style="
                color: #FFFFFF;
                font-size: 3.8rem;
                font-weight: 700;
                margin-bottom: 1.2rem;
                line-height: 1.15;
                text-shadow: 0px 3px 6px rgba(0,0,0,0.3);
            ">
                Planificador de Rutas de Valencia
            </h1>
            <h1 style="
                font-size: 1.6rem;
                color: white !important;
                max-width: 900px;
                margin: 0 auto 1rem auto;
                line-height: 1.65;
                font-weight: 300;
            ">
                Muévete por Valencia de forma fácil, fresca y ecológica: rutas a pie, en bici personal o con ValenBisi.
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.header("🎯 Propósito y Utilidad")
        st.markdown(
            """
            **Valen Fresc** está diseñado para mejorar la movilidad urbana, proporcionando opciones de rutas inteligentes, sostenibles y seguras.
            Nos enfocamos en promover métodos de transporte respetuosos con el entorno dentro de la ciudad y de cuidar a los ciudadanos bajo altas temperaturas, ofreciéndoles puntos estratégicos donde refrescarse.
            """
        )

        cols_about = st.columns(3, gap="large")
        with cols_about[0]:
            st.markdown("##### 🚶‍♂️ Rutas a Pie")
            st.markdown(
                "Encuentra el mejor camino peatonal entre dos puntos de Valencia."
            )
        with cols_about[1]:
            st.markdown("##### 🚴‍♂️ Rutas en Bicicleta Personal")
            st.markdown(
                "Encuentra la mejor ruta disponible para ir en carril bici o ciclovía por la ciudad de Valencia."
            )
        with cols_about[2]:
            st.markdown("##### 🚲 Integración ValenBisi")
            st.markdown(
                "Utiliza la red de bicicletas públicas ValenBisi para encontrar la mejor ruta y con las mejores estaciones disponibles."
            )

        st.markdown("---")

        st.subheader("🌡️ Adaptado al Clima: Rutas Inteligentes")
        st.markdown(
            """
            Frente al avance del **cambio climático** y las altas temperaturas en entornos urbanos, nuestra aplicación no solo planifica trayectos, sino que te cuida en el camino.

            - 🌳 **Priorizamos zonas con sombra**, detectando árboles cercanos a las calles.
            - 🚰 **Sugerimos paradas en fuentes públicas** según tu tipo de desplazamiento y la temperatura en ese preciso instante.
            - 🔁 **Adaptamos la frecuencia de descanso e hidratación** si el calor es extremo, protegiéndote de riesgos como el golpe de calor.

            Este enfoque climático convierte tu ruta en una experiencia **más saludable, sostenible y consciente del entorno**.
            """
        )
        st.markdown("---")

        # --- Section to promote the Route Planner ---
        st.header("✨ Visualiza tus Rutas")
        col_img_text_hp, col_img_main_hp = st.columns([0.55, 0.45], gap="large")
        with col_img_text_hp:
            st.markdown(
                """Nuestro mapa interactivo te permite:
                <ul>
                    <li>**Seleccionar puntos de inicio y fin** con un simple clic.</li>
                    <li>**Elegir tu modo de transporte preferido** (a pie, bicicleta personal, ValenBisi).</li>
                    <li>**Ver la ruta optimizada** claramente mostrada en el mapa.</li>
                </ul>
                ¡Empieza a planificar tu próximo viaje ahora!""",
                unsafe_allow_html=True,
            )
            if st.button(
                "¡Empieza a Planificar Tu Ruta!",
                use_container_width=False,
                type="primary",
            ):
                st.session_state.current_page_for_nav = "Planificador de Rutas"
                st.switch_page("pages/1_Implementation.py")

        st.markdown("---")
