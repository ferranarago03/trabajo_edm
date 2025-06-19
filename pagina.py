# Home.py
import streamlit as st

st.set_page_config(layout="wide")

st.title("Bienvenido a Mi Aplicación con Navegación")
st.write("Usa el menú desplegable para ir a diferentes secciones de la aplicación.")

# Crear el menú de selección
opciones_menu = {
    "Inicio": "Home.py", # Opcional, para que "Inicio" redirija a la propia Home
    "Acerca de": "pages/Acerca_de.py",
    "Contacto": "pages/Contacto.py",
    "Ver Datos": "pages/Datos.py"
}

# Usamos un selectbox. Cuando se selecciona una opción, Streamlit re-ejecuta el script.
# El valor por defecto es 'Inicio' para que no redirija inmediatamente al cargar.
seleccion = st.selectbox(
    "Selecciona una sección:",
    list(opciones_menu.keys()) # Obtenemos solo las claves para el selectbox
)

# Verificar si la selección actual no es la página 'Home' (o la que ya estamos)
# y luego usar st.switch_page
if seleccion != "Inicio": # Si el usuario seleccionó algo diferente de "Inicio"
    # Obtener la ruta del archivo correspondiente a la selección
    pagina_a_cambiar = opciones_menu[seleccion]
    st.write(f"Redirigiendo a: {pagina_a_cambiar}") # Para depuración
    st.switch_page(pagina_a_cambiar)

st.write("---")
st.info("Esta es la página de inicio. Usa el menú para navegar.")