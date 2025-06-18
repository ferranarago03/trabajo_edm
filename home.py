# esade_hub_app.py
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from pathlib import Path
import base64

# --- 0. NO MÁS MÓDULO DE AUTENTICACIÓN ---

# --- Define Paths to Local Assets ---
APP_DIR = Path(__file__).resolve().parent

LOGO_FILENAME = (
    "route_planner.png"  # You might want to rename this to a more generic app logo
)
LOGO_LOCAL_PATH_OBJ = APP_DIR / LOGO_FILENAME
LOGO_LOCAL_PATH_STR = str(LOGO_LOCAL_PATH_OBJ)

# Placeholder for an intro image if you want one, or remove if not needed
APP_INTRO_FILENAME = "aj_val.png"  # Renamed to be general
APP_INTRO_LOCAL_PATH_OBJ = APP_DIR / APP_INTRO_FILENAME

# --- 0.1 FAVICON SETUP ---
FAVICON_FILENAME = (
    "route_planner.png"  # Consider a more generic favicon like "favicon.png"
)
FAVICON_LOCAL_PATH_OBJ = APP_DIR / FAVICON_FILENAME

page_icon_to_use = "https://www.esade.edu/favicon.ico"  # Default fallback
if FAVICON_LOCAL_PATH_OBJ.is_file():
    page_icon_to_use = FAVICON_LOCAL_PATH_OBJ
else:
    print(
        f"DEBUG: Local favicon '{FAVICON_FILENAME}' not found at {FAVICON_LOCAL_PATH_OBJ}, using default URL."
    )

# --- 0.2 NO MÁS LOGIN GATEKEEPER ---
# if not gatekeeper(page_icon=page_icon_to_use, is_main_login_page=True):
#     pass

# --- IF WE REACH HERE, THE USER IS LOGGED IN (no longer relevant, always accessible) ---
# initialize_session_state() # No longer needed without auth


# Set initial page if not already set (retains functionality for direct access)
if "current_page_for_nav" not in st.session_state or Path(__file__).name == "home.py":
    st.session_state.current_page_for_nav = "Homepage"
    print("DEBUG: Setting current_page_for_nav to Homepage")


# --- 1. Page Configuration (FOR THE MAIN APP) ---
st.set_page_config(
    page_title="Route Planner App | Welcome",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=page_icon_to_use,
)


# --- 2. Load CSS ---
def load_main_app_css(file_name: str):
    css_path = APP_DIR / file_name
    if css_path.is_file():
        try:
            with open(css_path, encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading CSS from {css_path}: {e}")
    else:
        st.warning(
            f"CSS file '{file_name}' not found at {css_path}. Ensure it's in the '{APP_DIR.name}' directory."
        )


load_main_app_css("styles.css")


# --- Utility Function to Convert Image to Base64 ---
def get_image_as_base64(path_str: str) -> str | None:
    path_obj = Path(path_str)
    # 1) DEBUG: mostrar ruta y si existe
    st.write(f"DEBUG: buscando imagen en {path_obj}")
    st.write(f"DEBUG: ¿existe? {path_obj.is_file()}")
    if not path_obj.is_file():
        return None

    try:
        # 2) Leer y codificar
        with open(path_obj, "rb") as image_file:
            data = image_file.read()
            encoded_string = base64.b64encode(data).decode()

        ext = path_obj.suffix.lower()
        # 3) Mapear extensiones a MIME-types correctos
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".gif": "image/gif",
        }
        mime = mime_map.get(ext)
        if not mime:
            st.error(f"DEBUG: extensión no soportada: {ext}")
            return None

        return f"data:{mime};base64,{encoded_string}"

    except Exception as e:
        st.error(f"Error encoding image to base64: {e}")
        return None


# --- 3. Sidebar Content ---
with st.sidebar:
    if LOGO_LOCAL_PATH_OBJ.is_file():
        st.image(LOGO_LOCAL_PATH_STR, width=180)
    else:
        st.markdown(
            "<h2 style='text-align:center;'>ROUTE PLANNER</h2>", unsafe_allow_html=True
        )

    st.markdown("## Urban Mobility Insights")
    st.markdown(
        """
        Your go-to platform for planning sustainable routes within Valencia.
        Find optimal paths for walking, personal bikes, and ValenBisi.
        """
    )
    st.markdown("---")
    st.markdown("#### Quick Navigation")
    if st.button(
        "🗺️ Route Planner", use_container_width=True, key="sb_nav_route_planner"
    ):
        st.session_state.current_page_for_nav = "Route Planner"
        st.switch_page("pages/1_🗺️_Route_Planner.py")
    if st.button(
        "💡 Idea Presentation", use_container_width=True, key="sb_nav_idea_presentation"
    ):
        st.session_state.current_page_for_nav = "Idea Presentation"
        st.switch_page("pages/2_💡_Idea_Presentation.py")

    st.markdown("---")
    st.markdown("#### External Resources")
    st.markdown(
        "- [OpenStreetMap](https://www.openstreetmap.org/)", unsafe_allow_html=True
    )
    st.markdown(
        "- [ValenBisi Official Website](https://www.valenbisi.es/)",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    # NO Logout Button (removed)
    # if st.button(
    #     "Logout",
    #     use_container_width=True,
    #     key="logout_button_sidebar_main_v3",
    #     type="secondary",
    # ):
    #     do_logout()
    #     st.rerun()

    st.caption(f"© {pd.Timestamp.now().year} Route Planner | v1.0")
    st.caption("Sustainable Urban Mobility")

# --- 4. Top Horizontal Navigation Menu ---
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

options_list = ["Homepage", "Route Planner", "Idea Presentation"]

try:
    if (
        "current_page_for_nav" not in st.session_state
        or st.session_state.current_page_for_nav not in options_list
    ):
        st.session_state.current_page_for_nav = "Homepage"
    default_menu_index = options_list.index(st.session_state.current_page_for_nav)
except (ValueError, AttributeError, KeyError):
    st.session_state.current_page_for_nav = "Homepage"
    default_menu_index = 0


def nav_menu_changed(key_of_menu):
    st.session_state.current_page_for_nav = st.session_state[key_of_menu]


selected_page_from_menu = option_menu(
    menu_title=None,
    options=options_list,
    icons=["house-door-fill", "map", "lightbulb-fill"],
    menu_icon="list-ul",
    default_index=default_menu_index,
    orientation="horizontal",
    key="main_nav_menu_global_final_v4",
    styles=menu_styles,
    on_change=nav_menu_changed,
)

# --- 5. Handle Page Navigation (based on top menu selection) ---
if selected_page_from_menu != st.session_state.current_page_for_nav:
    st.session_state.current_page_for_nav = selected_page_from_menu

    if selected_page_from_menu == "Route Planner":
        st.switch_page("pages/1_🗺️_Route_Planner.py")
    elif selected_page_from_menu == "Idea Presentation":
        st.switch_page("pages/2_💡_Idea_Presentation.py")

# --- 6. Homepage Content (Only displayed if st.session_state.current_page_for_nav == "Homepage") ---
if st.session_state.current_page_for_nav == "Homepage":
    # --- Hero Section ---
    logo_base64_hero_str = get_image_as_base64(LOGO_LOCAL_PATH_STR)

    hero_section_logo_html = ""
    if logo_base64_hero_str:
        hero_section_logo_html = f"""
        <img src="{logo_base64_hero_str}" alt="App Logo" style="
            width: 240px;
            margin-bottom: 2.5rem;
            filter: brightness(0) invert(1);
        ">"""
    else:
        hero_section_logo_html = """<h2 style="color: #fff; font-size:2rem; margin-bottom: 2rem; letter-spacing: 2px; text-transform: uppercase;">ROUTE PLANNER</h2>"""

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
                Valencia Route Planner
            </h1>
            <h1 style="
                font-size: 1.6rem;
                color: white !important;
                max-width: 900px;
                margin: 0 auto 1rem auto;
                line-height: 1.65;
                font-weight: 300;
            ">
                Navigate Valencia effortlessly with optimized routes for walking, cycling, and public bikes.
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- About the Application Section ---
    with st.container():
        st.header("🎯 Purpose & Utility")
        st.markdown(
            """
            The **Valencia Route Planner** is designed to enhance urban mobility by providing intuitive and efficient routing options.
            We focus on promoting sustainable transportation methods within the city.
            """
        )
        cols_about = st.columns(3, gap="large")
        with cols_about[0]:
            st.markdown("##### 🚶‍♂️ Walking Routes")
            st.markdown(
                "Find the best pedestrian paths, ideal for exploring the city on foot."
            )
        with cols_about[1]:
            st.markdown("##### 🚴‍♂️ Personal Bicycle Routes")
            st.markdown(
                "Discover bicycle-friendly routes, perfect for your personal cycling adventures."
            )
        with cols_about[2]:
            st.markdown("##### 🚲 ValenBisi Integration")
            st.markdown(
                "Utilize Valencia's public bike-sharing network with integrated routing."
            )
        st.markdown(
            """
            <br>
            Our platform aims to make navigating Valencia greener, easier, and more enjoyable for everyone.
            """,
            unsafe_allow_html=True,
        )
    st.markdown("---")

    # --- Section to promote the Route Planner ---
    st.header("✨ Visualize Your Routes")
    col_img_text_hp, col_img_main_hp = st.columns([0.55, 0.45], gap="large")
    with col_img_text_hp:
        st.markdown(
            f"""Our interactive map allows you to:
        <ul>
            <li>**Select start and end points** with a simple click.</li>
            <li>**Choose your preferred mode of transport** (walking, personal bike, ValenBisi).</li>
            <li>**See the optimized route** clearly displayed on the map.</li>
        </ul>
        Start planning your next journey now!""",
            unsafe_allow_html=True,
        )
        if st.button(
            "Start Planning Your Route!", use_container_width=False, type="primary"
        ):
            st.session_state.current_page_for_nav = "Route Planner"
            st.switch_page("pages/1_🗺️_Route_Planner.py")

    with col_img_main_hp:
        if APP_INTRO_LOCAL_PATH_OBJ.is_file():
            st.image(
                APP_INTRO_LOCAL_PATH_OBJ,
                caption="Interactive Route Planner Preview.",
                use_container_width=True,
            )
        else:
            # Using a generic map image as placeholder if your specific image isn't found
            st.image(
                "https://images.unsplash.com/photo-1543360411-a83626e2e541?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                caption="Map Preview Not Found (Using Placeholder)",
                use_container_width=True,
            )
    st.markdown("---")
