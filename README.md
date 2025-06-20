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
A continuación mostraremos una pequeña introducción, para entender cómo está estructurado el proyecto:

```text
trabajo_edm/
├── 📂 app/                           # Código principal para la app Streamlit
│   ├── 📂 pages/                    # Páginas secundarias de la app
│   │   ├── ImplementaciOn.py
│   │   └── Planificador.py
│   ├── home.py
│   ├── nav.py
│   ├── styles.css
│   ├── route_planner.png
│   ├── upv.png
│   ├── ValenFresc.png
│   └── __pycache__/                 # Archivos compilados automáticamente

├── 📂 data/                         # Datos geoespaciales y CSVs
│   ├── arbratge-arbolado.csv
│   ├── cartografia-base-edificis-... .geojson
│   ├── fonts_publiques.csv
│   ├── itinerarios-ciclistas.geojson
│   ├── valenbisi_disponibilitat.csv
│   ├── valenbisi_stations.geojson
│   ├── valencia_cycling_network.graphml
│   ├── valencia_cycling_sombra.graphml
│   ├── valencia_walking_network.graphml
│   └── valencia_walking_sombra.graphml

├── 📂 notebooks/                    # Notebooks de prueba y procesamiento
│   ├── cache/
│   ├── creacion_ruta.ipynb
│   ├── creacion_sombra.ipynb
│   ├── descarga_archivo.ipynb
│   ├── obtencion_fuentes.ipynb
│   ├── obtencion_temp.ipynb
│   ├── pruebas_sombra.ipynb
│   └── ruta_valenbisi.ipynb

├── 📂 src/                          # Código Python del backend
│   ├── __pycache__/
│   ├── fountains.py                 # Obtención de rutas con fuentes
│   ├── routes.py                    # Cálculo de rutas con sombra
│   ├── temperature.py               # Obtención temperatura y tiempos
│   └── utils.py                     # Utilidades generales

├── 📄 README.md                     # 📖 Documentación del proyecto
├── 📄 requirements.txt              # 📦 Dependencias del proyecto
├── 📄 pyproject.toml                # ⚙️ Configuración del proyecto
├── 📄 uv.lock                       # 📌 Bloqueo de versiones
└── 📂 .venv/                        # 🐍 Entorno virtual (no se versiona)

```
## 🚀 Cómo Usar la aplicación en local
1. Clona el repositorio:
   ```bash
   git clone https://github.com/ferranarago03/trabajo_edm.git
   cd trabajo_edm
   ```
2. Instala el entorno 
   ```bash
   # Crear entorno virtual (usando uv)
    uv venv .venv

    # Activar el entorno:
    ## Linux/MacOS:
    source .venv/bin/activate

    ## Windows (PowerShell):
    .\.venv\Scripts\activate
   ```
3. Instala dependencias con uv
   ```bash
   ## Con requirements.txt
   uv pip install -r requirements.txt

   ## Con pyproject.toml
   uv pip install .  # Instala en modo editable (recomendado para desarrollo)
   ```
4. Sincronizar dependencias
   ```bash
   uv pip sync requirements.lock  # Bloquea versiones exactas
   ```
5. Ejecuta la aplicación desde la ruta padre, es decir, desde trabajo_edm:
   ```bash
   streamlit run .\home.py
   ```
6. ¡Abre el enlace que te proporciona Streamlit en tu navegador!
   
   ## 🔮 Mejoras Futuras

- 🏢 **Integrar altura de edificios** para calcular sombra en tiempo real.
- 💧 **Considerar humedad y sensación térmica** para priorizar rutas.
- 🚦 **Analizar tiempos reales de desplazamiento** considerando semáforos y zonas de espera.

## 🤝 Contribuciones
¡Toda colaboración es bienvenida!
Abre un issue o envía un pull request si quieres proponer cambios, mejoras o nuevas funcionalidades.

## 📧  Contacto 
- [faraaus@etsinf.upv.es](mailto:faraaus@etsinf.upv.es)
- [cnavest@etsinf.upv.es](mailto:cnavest@etsinf.upv.es)
- [atarsor@etsinf.upv.es](mailto:atarsor@etsinf.upv.es)