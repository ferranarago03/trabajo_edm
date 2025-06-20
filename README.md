# 🌳 ValenFresc 

## 📝 Descripción
Aplicación web que calcula rutas urbanas sostenibles en Valencia minimizando la exposición al calor. Tiene en cuenta la sombra de los árboles, la ubicación de fuentes públicas, estaciones ValenBisi, temperatura en tiempo real y carriles bici, para ofrecer trayectos más saludables y confortables.

## 🧠 Origen de la Idea
La idea surge ante la creciente problemática de las altas temperaturas en las ciudades mediterráneas y la necesidad de ofrecer trayectos que prioricen sombra y puntos de agua potable. Aprovechando datos geoespaciales y meteorológicos abiertos, la herramienta propone rutas que mejoran el confort y promueven la movilidad sostenible.

## ✨ Características
- 📍 Obtención de datos de OpenStreetMap y Open Data Valencia (árboles, fuentes públicas, estaciones ValenBisi).
- 🌡️ Cálculo dinámico del peso por sombra y temperatura actual (API Open Meteo).
- 🧭 Rutas personalizadas a pie o en bicicleta, priorizando zonas sombreadas y estaciones ValenBisi con disponibilidad.
- 💧 Identificación automática de fuentes públicas a lo largo del recorrido según la temperatura.
- 🗺️ Visualización interactiva en un mapa (Folium + Streamlit) con distancia, temperatura y paradas recomendadas.

## 🎯 Público Objetivo
- **Residentes de Valencia** que desean moverse por la ciudad evitando zonas muy soleadas.
- **Turistas** que buscan recorrer la ciudad a pie o en bicicleta con mayor comodidad.
- **Urbanistas** interesados en analizar rutas populares y puntos de calor para planificar mejoras.

## 🛠️ Tecnologías Utilizadas
- 🐍 **Python** como lenguaje principal.
- 🕸️ **Streamlit** para la aplicación web.
- 🗺️ **Folium** para la visualización geográfica.
- 🧮 **OSMnx** para trabajar con redes de calles desde OpenStreetMap.
- 🌐 **API Open Data Valencia** para árboles, fuentes y estaciones ValenBisi.
- 🌡️ **API Open-Meteo** para datos meteorológicos.

## 📂 Estructura del Proyecto

├── data/ # Datos estáticos o generados
├── src/ # Módulos Python
├── app.py # Aplicación Streamlit
├── requirements.txt
├── README.md # Este archivo
