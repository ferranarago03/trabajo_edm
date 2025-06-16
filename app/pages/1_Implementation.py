# pages/1_Implementation.py
import streamlit as st
from streamlit_folium import st_folium
import folium
import sys
import osmnx as ox

# Add the src directory to the system path
sys.path.append("./src/")

# Assuming get_route is defined in utils.py inside src/
from utils import get_route

st.title("Define Your Route's Start and End Points")

# --- Sidebar Controls ---
st.sidebar.header("Route Type")
# Selectbox to choose the type of route
route_options = ["Walking", "Personal Bicycle", "ValenBisi"]
type_route = st.sidebar.selectbox(
    "What type of route do you want to define?", route_options
)

st.sidebar.header("Select Route Point")
# Radio button to choose between start and end point
point_options = ["Start", "End"]
point_to_set = st.sidebar.radio("Which point do you want to set?", point_options)

# --- Initialize Session State for Coordinates ---
if "start" not in st.session_state:
    st.session_state.start = None
if "end" not in st.session_state:
    st.session_state.end = None

# --- Create the Map ---
# Optionally center the map on the last known point
center = [39.4699, -0.3763]  # Default to Valencia's center
if st.session_state.start:
    center = [st.session_state.start["lat"], st.session_state.start["lng"]]
elif st.session_state.end:
    center = [st.session_state.end["lat"], st.session_state.end["lng"]]

m = folium.Map(location=center, zoom_start=15)

# --- Add Saved Markers to the Map ---
if st.session_state.start:
    folium.Marker(
        [st.session_state.start["lat"], st.session_state.start["lng"]],
        popup="Start",
        icon=folium.Icon(color="green"),
    ).add_to(m)
if st.session_state.end:
    folium.Marker(
        [st.session_state.end["lat"], st.session_state.end["lng"]],
        popup="End",
        icon=folium.Icon(color="red"),
    ).add_to(m)

# --- Draw the Route if Both Points are Set ---
if st.session_state.start and st.session_state.end:
    # Load graphs (ensure these files exist in your data/ directory)
    # You might want to load these once outside this if block if they are large
    try:
        graph_cycling = ox.load_graphml("data/valencia_cycling_network.graphml")
        graph_walking = ox.load_graphml("data/valencia_walking_network.graphml")
    except FileNotFoundError:
        st.error(
            "Error: Network graph files not found. Please ensure 'valencia_cycling_network.graphml' and 'valencia_walking_network.graphml' are in the 'data/' directory."
        )
        st.stop()  # Stop execution if files are missing

    route = None
    if type_route == "Walking":
        route = get_route(
            (st.session_state.start["lat"], st.session_state.start["lng"]),
            (st.session_state.end["lat"], st.session_state.end["lng"]),
            graph_walking,
        )
    elif type_route == "Personal Bicycle" or type_route == "ValenBisi":
        # For now, both bicycle types use the same graph.
        # You might implement specific logic for ValenBisi later if needed (e.g., station proximity).
        route = get_route(
            (st.session_state.start["lat"], st.session_state.start["lng"]),
            (st.session_state.end["lat"], st.session_state.end["lng"]),
            graph_cycling,
        )

    if route:
        # Determine which graph to use for node coordinates
        graph_to_use = graph_walking if type_route == "Walking" else graph_cycling
        folium.PolyLine(
            locations=[
                [graph_to_use.nodes[node]["y"], graph_to_use.nodes[node]["x"]]
                for node in route
            ],
            color="blue",
            weight=5,
            opacity=0.7,
        ).add_to(m)
        st.success("Route successfully generated!")
    else:
        st.warning(
            "Could not find a route between the selected points for the chosen transport type. Please try different points."
        )


# --- Plugin to Capture Clicks and Place a Temporary Marker ---
m.add_child(
    folium.ClickForMarker(
        popup=f"Select the {point_to_set.lower()} of the route",
    )
)

# --- Render the Map and Capture Clicks ---
map_data = st_folium(m, width=700, height=500)

# --- Save Clicked Coordinates ---
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]
    if point_to_set == "Start":
        st.session_state.start = {"lat": lat, "lng": lng}
        st.success(f"**Start** point saved at {lat:.6f}, {lng:.6f}")
    else:
        st.session_state.end = {"lat": lat, "lng": lng}
        st.success(f"**End** point saved at {lat:.6f}, {lng:.6f}")

    # Rerun the app to refresh the map with new markers/lines
    st.rerun()
