import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

from datetime import datetime as dt


def get_temperature_data(now: dt) -> int:
    """
    Fetches temperature data for a specific day using the Open-Meteo API.

    Parameters:
        day (datetime): The date for which to fetch temperature data in 'YYYY-MM-DD' format.

    Returns:
        int: The temperature in degrees Celsius for the specified day at the current hour.
    """

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 39.4739,
        "longitude": -0.3797,
        "hourly": "temperature_2m",
        "start_date": now.strftime("%Y-%m-%d"),
        "end_date": now.strftime("%Y-%m-%d"),
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    now = pd.Timestamp(dt(now.year, now.month, now.day, now.hour, 0, 0), tz="UTC")

    temp = hourly_dataframe[hourly_dataframe["date"] == now]["temperature_2m"].values[0]

    return temp
