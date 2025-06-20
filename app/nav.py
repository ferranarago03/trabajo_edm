import streamlit as st
from streamlit_option_menu import option_menu


def show_nav_menu(current_page: str = None):
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

    options_list = [
        "Página Principal",
        "Implementación de la Idea",
        "Planificador de Rutas",
    ]

    selected_page_from_menu = option_menu(
        menu_title=None,
        options=options_list,
        icons=["house-door-fill", "lightbulb-fill", "map"],
        menu_icon="list-ul",
        default_index=options_list.index(current_page) if current_page else 0,
        orientation="horizontal",
        key="main_nav_menu_global_final_v4",
        styles=menu_styles,
    )

    if selected_page_from_menu != st.session_state.current_page_for_nav:
        st.session_state.current_page_for_nav = selected_page_from_menu
        if selected_page_from_menu == "Planificador de Rutas":
            st.switch_page("pages/Planificador.py")
        elif selected_page_from_menu == "Implementación de la Idea":
            st.switch_page("pages/Implementación.py")
        elif selected_page_from_menu == "Página Principal":
            st.switch_page("home.py")
