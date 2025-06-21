# 🌳 Valen Fresc 

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
│   ├── ValenFresc.png
│   └── __pycache__/                 # Archivos compilados automáticamente
│
├── 📂 data/                         # Datos geoespaciales y CSVs
│   ├── arbratge-arbolado.csv
│   ├── fonts_publiques.csv
│   ├── valencia_cycling_network.graphml
│   ├── valencia_cycling_sombra.graphml
│   ├── valencia_walking_network.graphml
│   └── valencia_walking_sombra.graphml
│
├── 📂 notebooks/                    # Notebooks de prueba y procesamiento
│   ├── cache/
│   ├── creacion_ruta.ipynb
│   ├── creacion_sombra.ipynb
│   ├── descarga_archivo.ipynb
│   ├── obtencion_fuentes.ipynb
│   ├── obtencion_temp.ipynb
│   └── ruta_valenbisi.ipynb
│
├── 📂 src/                          # Código Python del backend
│   ├── __pycache__/
│   ├── fountains.py                 # Obtención de rutas con fuentes
│   ├── routes.py                    # Cálculo de rutas con sombra
│   ├── temperature.py               # Obtención temperatura y tiempos
│   └── utils.py                     # Utilidades generales
│
├── 📄 README.md                     # 📖 Documentación del proyecto
├── 📄 requirements.txt              # 📦 Dependencias del proyecto
├── 📄 pyproject.toml                # ⚙️ Configuración del proyecto
└── 📄 uv.lock                       # 📌 Bloqueo de versiones

```
## 🚀 Cómo Usar la aplicación en local
1. Clona el repositorio:
   ```bash
   git clone https://github.com/ferranarago03/trabajo_edm.git
   cd trabajo_edm
   ```
2. Instala el entorno 
   1. Mediante `uv` (recomendado):
      ```bash
      # Crear entorno virtual
      uv sync

      # Activar el entorno:
      ## Linux/MacOS:
      source .venv/bin/activate

      ## Windows (PowerShell):
      .\.venv\Scripts\activate
      ```
   2. O con `venv` (alternativa):

      ```bash
      # Crear entorno virtual
      python -m venv .venv
      
      # Activar el entorno:
      ## Linux/MacOS:
      source .venv/bin/activate
      
      ## Windows (PowerShell):
      .\.venv\Scripts\activate
      ```
3. Instala dependencias con uv
4. 
   El comando `uv sync` instalará todas las dependencias necesarias para el proyecto.
   ```bash
   uv sync
   ```
   O si prefieres usar `pip`:
   ```bash
   pip install -r requirements.txt
   ```
5. Descarga los datos necesarios:

   Los datos se encuentra en la carpeta `data/`, execeptuando de una archivo más pesado que se descargará automáticamente al ejecutar la aplicación por primera vez.

   En caso de no disponer de los datos, puedes disponer de todos ellos de la siguiente manera:
   
   1. Ejecutar el notebook `descarga_archivo.ipynb` para descargar los grafos de OSMnx necesarios y la información de las fuentes públicas.
   2. Descargar el archivo `arbratge-arbolado.csv` desde el [Portal de Datos Abiertos de Valencia](https://valencia.opendatasoft.com/explore/dataset/arbratge-arbolado/export/) y guardarlo en la carpeta `data/`. Este archivo no se descarga automáticamente debido a su tamaño.
   3. Ejecutar el notebook `creacion_sombra.ipynb` para crear los grafos con la información relativa a la sombra de los árboles.

6. Ejecuta la aplicación desde la ruta padre, es decir, desde trabajo_edm:
   ```bash
   streamlit run .\home.py
   ```
7. ¡Abre el enlace que te proporciona Streamlit en tu navegador!
   
   ## 🔮 Futuras Ampliaciones

- 🏢 **Integrar altura de edificios** para calcular sombra en tiempo real.
- 💧 **Considerar humedad y sensación térmica** para priorizar rutas.
- 🚦 **Analizar tiempos reales de desplazamiento** considerando semáforos y zonas de espera.

## 🤝 Contribuciones
¡Toda colaboración es bienvenida!
Abre un issue o envía un pull request si quieres proponer cambios, mejoras o nuevas funcionalidades.

## 📧  Contacto 
- Ferran Aragó Ausina ~ [faraaus@etsinf.upv.es](mailto:faraaus@etsinf.upv.es)
- Carles Navarro Esteve ~ [cnavest@etsinf.upv.es](mailto:cnavest@etsinf.upv.es)
- Aleixandre Tarrasó Sorní ~ [atarsor@etsinf.upv.es](mailto:atarsor@etsinf.upv.es)