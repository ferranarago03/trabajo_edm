import osmnx as ox
import pandas as pd
import requests
import geopandas as gpd


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
        print(f"Total records found: {total_records}")

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


def get_valenbisi_stations(valenbisi_data):
    """
    Extract Valenbisi stations from the Valenbisi data.

    Parameters:
        valenbisi_data (DataFrame): A DataFrame containing Valenbisi data.

    Returns:
        GeoDataFrame: A GeoDataFrame containing the Valenbisi stations.
    """

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(valenbisi_data, geometry=valenbisi_data["geometry"])
    gdf.set_crs(epsg=4326, inplace=True)  # Set the coordinate reference system

    return gdf


def get_nearest_cycle_station(graph, geovalenbisi):
    """
    Find the nearest point in the graph to each Valenbisi station.
    Parameters:
        graph: The cycling network graph.
        geovalenbisi (GeoDataFrame): A GeoDataFrame containing Valenbisi stations.
    Returns:
        GeoDataFrame: A GeoDataFrame with the nearest points in the graph to each Valenbisi station.
    """
    nearest_points = []
    for _, row in geovalenbisi.iterrows():
        point = row.geometry
        nearest_node = ox.distance.nearest_nodes(graph, point.x, point.y)
        nearest_points.append(nearest_node)

    geovalenbisi["nearest_node"] = nearest_points
    return geovalenbisi
