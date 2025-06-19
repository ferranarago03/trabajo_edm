import osmnx as ox
import folium

import sys

sys.path.append("./src/")
from utils import get_nearest_station, get_distance


def get_route(start, end, graph, range_temp="length"):
    """
    Get the route between two nodes in the graph.

    Parameters:
        start(tuple): Tuple of coordenates for the start point.
        end: Tuple of coordinates for the end point.
        graph: The cycling network graph.
        range: Temperature range for obtaining edge weight.

    Returns:
        list: A list of nodes representing the route.
    """
    from_node = ox.distance.nearest_nodes(graph, start[1], start[0])
    to_node = ox.distance.nearest_nodes(graph, end[1], end[0])
    distancia = get_distance(start, end)
    route = ox.shortest_path(graph, from_node, to_node, weight=range_temp)
    if not route:
        print("No route found.")
        return [], 0

    distancia = 0
    for i in range(len(route) - 1):
        edge_data = graph.get_edge_data(route[i], route[i + 1])
        if edge_data and "length" in edge_data[0]:
            distancia += edge_data[0]["length"]
        else:
            distancia += get_distance(
                (graph.nodes[route[i]]["y"], graph.nodes[route[i]]["x"]),
                (graph.nodes[route[i + 1]]["y"], graph.nodes[route[i + 1]]["x"]),
            )
    return route, distancia


def print_route(route, graph, map, color="blue"):
    """
    Print the route on the map.

    Parameters:
        route (list): List of nodes in the route.
        graph: The graph containing the nodes.
        map: The folium map to draw the route on.
        color (str): Color of the route line on the map.
    """
    if not route:
        print("No route found.")
        return

    for i in range(len(route) - 1):
        edge_data = graph.get_edge_data(route[i], route[i + 1])
        if edge_data and "geometry" in edge_data[0]:
            geom = edge_data[0]["geometry"]
            folium.PolyLine(
                locations=[(point[1], point[0]) for point in geom.coords],
                color=color,
                weight=5,
            ).add_to(map)
        else:
            folium.PolyLine(
                locations=[
                    (
                        graph.nodes[route[i]]["y"],
                        graph.nodes[route[i]]["x"],
                    ),
                    (
                        graph.nodes[route[i + 1]]["y"],
                        graph.nodes[route[i + 1]]["x"],
                    ),
                ],
                color=color,
                weight=5,
            ).add_to(map)


def get_valenbisi_route(
    start, end, cycling_graph, walking_graph, valenbisi_stations, range_temp="length"
):
    """
    Get the Valenbisi route from start to end using the cycling network graph.

    Parameters:
        start(tuple): Tuple of coordinates for the start point.
        end(tuple): Tuple of coordinates for the end point.
        cycling_graph: The cycling network graph.
        walking_graph: The walking network graph.
        valenbisi_stations(geoDataFrame): A GeoDataFrame containing Valenbisi stations.
        range: Temperature range for obtaining edge weight.


    Returns:
        tuple: A tuple containing three lists:
            - The walking route from the start to the nearest Valenbisi station.
            - The cycling route between the two Valenbisi stations.
            - The walking route from the nearest Valenbisi station to the end point.
            - The nearest Valenbisi station to the start point.
            - The nearest Valenbisi station to the end point.
    """

    threshold = 0.0001

    cycling_ini_node = ox.distance.nearest_nodes(cycling_graph, X=start[1], Y=start[0])

    cycling_end_node = ox.distance.nearest_nodes(cycling_graph, X=end[1], Y=end[0])

    ini_valenbisi_station = valenbisi_stations[
        valenbisi_stations["available"] > 0
    ].copy()
    end_valenbisi_station = valenbisi_stations[valenbisi_stations["free"] > 0].copy()

    ini_station = get_nearest_station(
        (
            cycling_graph.nodes[cycling_ini_node]["y"],
            cycling_graph.nodes[cycling_ini_node]["x"],
        ),
        ini_valenbisi_station,
    )
    end_station = get_nearest_station(
        (
            cycling_graph.nodes[cycling_end_node]["y"],
            cycling_graph.nodes[cycling_end_node]["x"],
        ),
        end_valenbisi_station,
    )

    ini_station_loc = ini_station["geo_point_2d"]
    end_station_loc = end_station["geo_point_2d"]

    ini_walking_route, dist1 = get_route(
        start,
        (ini_station_loc["lat"], ini_station_loc["lon"]),
        walking_graph,
        range_temp,
    )
    end_walking_route, dist2 = get_route(
        (end_station_loc["lat"], end_station_loc["lon"]), end, walking_graph, range_temp
    )
    cycling_route, dist3 = get_route(
        (ini_station_loc["lat"], ini_station_loc["lon"]),
        (end_station_loc["lat"], end_station_loc["lon"]),
        cycling_graph,
        range_temp,
    )

    dist_ini_station = ox.distance.euclidean(
        ini_station_loc["lat"],
        ini_station_loc["lon"],
        cycling_graph.nodes[cycling_route[0]]["y"],
        cycling_graph.nodes[cycling_route[0]]["x"],
    )

    dist_end_station = ox.distance.euclidean(
        end_station_loc["lat"],
        end_station_loc["lon"],
        cycling_graph.nodes[cycling_route[-1]]["y"],
        cycling_graph.nodes[cycling_route[-1]]["x"],
    )

    if dist_ini_station > threshold:
        inter_ini, d_aux = get_route(
            (ini_station_loc["lat"], ini_station_loc["lon"]),
            (
                cycling_graph.nodes[cycling_route[0]]["y"],
                cycling_graph.nodes[cycling_route[0]]["x"],
            ),
            walking_graph,
            range_temp,
        )
        ini_walking_route.extend(inter_ini)
        dist1 += d_aux
    if dist_end_station > threshold:
        inter_end, d_aux = get_route(
            (
                cycling_graph.nodes[cycling_route[-1]]["y"],
                cycling_graph.nodes[cycling_route[-1]]["x"],
            ),
            (end_station_loc["lat"], end_station_loc["lon"]),
            walking_graph,
            range_temp,
        )
        end_walking_route = inter_end + end_walking_route
        dist2 += d_aux
    return (
        ini_walking_route,
        dist1,
        cycling_route,
        dist3,
        end_walking_route,
        dist2,
        ini_station,
        end_station,
    )


def get_cycling_route(start, end, cycling_graph, walking_graph, range_temp="length"):
    """
    Get the mixed route from start to end using walking and cycling network graphs.

    Parameters:
        start (tuple): (lat, lon) start point.
        end (tuple): (lat, lon) end point.
        cycling_graph: OSMnx cycling graph.
        walking_graph: OSMnx walking graph.

    Returns:
        tuple:
            - walking route from start to cycling network
            - distance of that walking route
            - cycling route
            - distance of that cycling route
            - walking route from cycling network to end
            - distance of that walking route
    """

    nodo_ini_bike = ox.distance.nearest_nodes(cycling_graph, X=start[1], Y=start[0])
    nodo_end_bike = ox.distance.nearest_nodes(cycling_graph, X=end[1], Y=end[0])

    ini_walking_route, dist1 = get_route(
        start,
        (
            cycling_graph.nodes[nodo_ini_bike]["y"],
            cycling_graph.nodes[nodo_ini_bike]["x"],
        ),
        walking_graph,
        range_temp,
    )

    cycling_route, dist2 = get_route(
        (
            cycling_graph.nodes[nodo_ini_bike]["y"],
            cycling_graph.nodes[nodo_ini_bike]["x"],
        ),
        (
            cycling_graph.nodes[nodo_end_bike]["y"],
            cycling_graph.nodes[nodo_end_bike]["x"],
        ),
        cycling_graph,
        range_temp,
    )

    end_walking_route, dist3 = get_route(
        (
            cycling_graph.nodes[nodo_end_bike]["y"],
            cycling_graph.nodes[nodo_end_bike]["x"],
        ),
        end,
        walking_graph,
        range_temp,
    )

    return (
        ini_walking_route,
        dist1,
        cycling_route,
        dist2,
        end_walking_route,
        dist3,
    )


def print_stations(ini, end, map):
    ini_station_loc = ini["geo_point_2d"]
    end_station_loc = end["geo_point_2d"]
    folium.Marker(
        location=(ini_station_loc["lat"], ini_station_loc["lon"]),
        popup=f"Start Station.<br>Available Bikes: {ini['available']}",
        icon=folium.Icon(color="green", icon="bicycle", prefix="fa"),
    ).add_to(map)

    folium.Marker(
        location=(end_station_loc["lat"], end_station_loc["lon"]),
        popup=f"End Station<br>Available Places: {end['free']}",
        icon=folium.Icon(color="red", icon="home"),
    ).add_to(map)
