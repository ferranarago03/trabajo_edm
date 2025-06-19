import numpy as np
from math import radians, sin, cos, sqrt, atan2
from scipy.spatial import cKDTree
import folium


def get_nearest_water_fountains_on_route(
    graph, distancia, route_nodes, type_displacement, temperatura, fuentes_publicas_gpd
):
    """
    Find the nearest public water fountains along a given route, using pre-loaded fountain GeoDataFrame.

    Parameters:
        graph: The cycling network graph.
        distancia (float): Total length of the route in meters.
        route_nodes (list): A list of nodes representing the route.
        type_displacement (str): "Caminando", "En Bicicleta" or "En ValenBisi".
        temperatura (float): Current temperature in °C.
        fuentes_publicas_gpd (GeoDataFrame): GeoDataFrame of public fountains with geometry column.

    Returns:
        list: A list of node IDs for fountains within max_distance of each stop point.
    """
    fountain_nodes = fuentes_publicas_gpd.index.to_list()
    fountain_coords = np.array([(pt.y, pt.x) for pt in fuentes_publicas_gpd.geometry])
    tree = cKDTree(fountain_coords)

    def haversine(a, b):
        R = 6_371_000  # Earth radius in meters
        lat1, lon1 = map(radians, a)
        lat2, lon2 = map(radians, b)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        u = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 2 * R * atan2(sqrt(u), sqrt(1 - u))

    # Temperature-based stop frequency
    freq_config = {
        "frio": {"min": -50, "max": 10, "Caminando": 10, "En Bicicleta": 12},
        "ideal": {"min": 15, "max": 25, "Caminando": 7, "En Bicicleta": 9},
        "calor_extremo": {"min": 30, "max": 50, "Caminando": 4, "En Bicicleta": 6},
    }

    def obtener_frecuencia():
        if temperatura < 15:
            return freq_config["frio"][type_displacement]
        elif 15 <= temperatura <= 25:
            return freq_config["ideal"][type_displacement]
        elif temperatura > 25:
            return freq_config["calor_extremo"][type_displacement]
        else:
            return None

    # Determine speed and max_distance
    if type_displacement == "Caminando":
        velocidad = 1.0  # m/s
        max_distance = 100  # meters
    else:
        velocidad = 3.0  # m/s (both bicycle and ValenBisi)
        max_distance = 350  # meters

    frecuencia = obtener_frecuencia()
    if frecuencia is None:
        return [], 0

    n_paradas = int(distancia / (velocidad * 60 * frecuencia))
    if n_paradas <= 0:
        return [], 0

    d = distancia / n_paradas
    resultados = []

    d_accum = 0.0
    parada = 1

    for i in range(len(route_nodes) - 1):
        edge_info = graph.get_edge_data(route_nodes[i], route_nodes[i + 1])
        if not edge_info or "length" not in edge_info[0]:
            continue

        d_accum += edge_info[0]["length"]
        if d_accum >= parada * d:
            _, idx = tree.query(
                [(graph.nodes[route_nodes[i]]["y"], graph.nodes[route_nodes[i]]["x"])],
                k=1,
            )
            fountain_idx = fountain_nodes[idx[0]]
            fountain_pt = fuentes_publicas_gpd.loc[fountain_idx].geometry
            d_m = haversine(
                (graph.nodes[route_nodes[i]]["y"], graph.nodes[route_nodes[i]]["x"]),
                (fountain_pt.y, fountain_pt.x),
            )
            parada += 1
            if d_m <= max_distance:
                resultados.append(fountain_idx)

    return resultados, n_paradas


def print_fountains(fountains, public_fountains_gpd, map):
    """
    Print the fountains on the map.

    Parameters:
        fountains (list): List of fountain node IDs.
        public_fountains_gpd (GeoDataFrame): GeoDataFrame of public fountains with geometry column.
        map: The folium map to draw the fountains on.
    """
    for idx in fountains:
        calle = public_fountains_gpd.loc[idx, "calle"]
        pt = public_fountains_gpd.loc[idx].geometry
        folium.Marker(
            location=(pt.y, pt.x),  # latitud, longitud
            popup=f"Fuente calle {calle}",
            icon=folium.Icon(color="blue", icon="tint", prefix="fa"),
        ).add_to(map)
