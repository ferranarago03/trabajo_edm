import osmnx as ox
import pandas as pd
import requests
import geopandas as gpd
from shapely.geometry import Point
import math
import os


def get_walking_network(place_name: str):
    """
    Get the walking network for a specified place using OSMnx.

    Parameters:
        place_name (str): The name of the place to get the walking network for.

    Returns:
        graph: A directed graph representing the walking network.
    """
    graph = ox.graph_from_place(place_name, network_type="walk")

    return graph


def get_cycling_network(place_name: str):
    """
    Get the cycling network for a specified place using OSMnx.

    Parameters:
        place_name (str): The name of the place to get the cycling network for.

    Returns:
        graph: A directed graph representing the cycling network.
    """
    graph = ox.graph_from_place(
        place_name,
        network_type="bike",
        custom_filter='["highway"~"cycleway|footway|pedestrian"]',
    )

    return graph


def get_valencian_open_data(url: str, params: dict = None):
    """
    Fetch open data from the Valencia City Council's open data portal.

    Returns:
        dict: A dictionary containing the fetched data.
    """
    df = pd.DataFrame()
    response = requests.get(url, params=params)

    if response.status_code == 200:
        total_records = response.json().get("total_count")

        for start in range(0, total_records, params.get("rows", 10)):
            params["start"] = start
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                records = data.get("results", [])
                df = pd.concat([df, pd.DataFrame(records)], ignore_index=True)
            else:
                raise Exception(
                    f"Failed to fetch data: {response.status_code}\n{response.text}"
                )

        return df
    else:
        raise Exception(
            f"Failed to fetch data: {response.status_code}\n{response.text}"
        )


def get_gdf(df):
    """
    Extract a GeoDataFrame from DataFrame containing teh geometry column.

    Parameters:
        df (DataFrame): A DataFrame containing the column geometry.

    Returns:
        GeoDataFrame: A GeoDataFrame of the given DataFrame.
    """

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=df["geometry"])
    gdf.set_crs(epsg=4326, inplace=True)

    return gdf


def get_nearest_station(point, gdf):
    """
    Find the nearest station to a given point using Euclidean distance
    after reprojecting the data to a metric CRS.

    Parameters:
        point (tuple): Tuple of coordinates (lat, lon) for the query point.
        gdf (GeoDataFrame): GeoDataFrame of stations with geometry column in EPSG:4326.

    Returns:
        GeoSeries: Row corresponding to the nearest station, including the distance in meters.
    """

    gdf_proj = gdf.to_crs(epsg=25830)
    point_geom = (
        gpd.GeoSeries([Point(point[1], point[0])], crs="EPSG:4326")
        .to_crs(epsg=25830)
        .iloc[0]
    )
    gdf_proj["distance"] = gdf_proj.distance(point_geom)
    nearest_row = gdf_proj.loc[gdf_proj["distance"].idxmin()]
    return nearest_row


def get_distance(start, end):
    """
    Calculate the distance between two geographic points.

    Parameters:
        start (tuple): (lat, lon) in decimal degrees.
        end   (tuple): (lat, lon) in decimal degrees.

    Returns:
        deg_dist (float): Euclidean distance in decimal degrees.
        gc_dist_m (float): Great-circle distance in meters.
    """
    lat1, lon1 = map(math.radians, start)
    lat2, lon2 = map(math.radians, end)

    # 2. Haversine (great-circle) in meters
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000  # Earth radius in meters
    gc_dist_m = R * c

    return gc_dist_m


def read_graph(file_path: str):
    """
    Read a graph from a file.

    Parameters:
        file_path (str): Path to the graph file.

    Returns:
        graph: The loaded graph.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Graph file not found: {file_path}")

    graph = ox.load_graphml(file_path)
    # Cambiar el tipo de valor de algunos atributos de aristas
    tramos = [
        (0, 5),
        (5, 10),
        (10, 15),
        (15, 20),
        (20, 25),
        (25, 30),
        (30, 35),
        (35, 40),
    ]
    for u, v, data in graph.edges(data=True):
        for tramo in tramos:
            t_str = f"peso_{tramo[0]}_{tramo[1]}"
            if t_str in data:
                data[t_str] = float(data[t_str])
    graph = ox.project_graph(graph, to_crs="EPSG:4326")
    return graph
