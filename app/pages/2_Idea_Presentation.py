# pages/2_Idea_Presentation.py
import streamlit as st

st.set_page_config(
    page_title="Idea Presentation",
    page_icon="💡",
    layout="centered",
)

st.title("Idea Presentation: Smart Urban Mobility in Valencia")

st.markdown("""
---
### Project Vision
Our project aims to enhance urban mobility in Valencia by providing an intuitive and efficient route planning application.
We focus on sustainable transportation methods, promoting walking and cycling as primary modes of travel.

### Key Features
* **Multi-modal Route Planning**: Users can choose between walking, personal bicycle, and ValenBisi routes.
* **Interactive Map Interface**: Easy selection of start and end points directly on a Folium-powered map.
* **Optimized Routing**: Utilizes OpenStreetMap data and `osmnx` for intelligent pathfinding based on network topology and chosen transport type.
* **User-Friendly Experience**: A simple and clean interface designed for all users.

### Target Audience
This application is designed for:
* **Valencia Residents**: Daily commuters looking for efficient and sustainable travel options.
* **Tourists**: Visitors wanting to explore Valencia on foot or by bike.
* **Urban Planners**: To analyze popular routes and identify areas for infrastructure improvement.

### Technologies Used
* **Streamlit**: For creating the interactive web application.
* **Folium**: For visualizing geographic data and interactive maps.
* **OSMnx**: For downloading, constructing, analyzing, and visualizing street networks from OpenStreetMap.
* **Python**: The core programming language.

### Future Enhancements
* **Real-time Traffic/Availability**: Integrate live data for ValenBisi station availability or traffic conditions.
* **Accessibility Options**: Consider routes optimized for users with mobility challenges.
* **Route Customization**: Allow users to specify preferences like "avoid hills" or "most scenic route".
* **Estimated Travel Time and Distance**: Display calculated travel time and distance for the generated route.
* **Public Transport Integration**: Combine walking/cycling with public transport options.

---
""")

st.image(
    "https://images.unsplash.com/photo-1549429780-e4b097b6a18d?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    caption="Cycling in the city, photo by Dan Visan on Unsplash",
)
