def UserFunction(id, eliona):
    from meteostat import Point, Daily
    from datetime import datetime, timedelta
    import pandas as pd

    # Variables
    # ------------------------------------------------#
    # Latitude & Longitude of the location
    location = Point(47.5767, 7.5801)

    # GAI of the Asset where the data should go
    gai = "WSJ-Test-HGT"

    # Attribute names for degree days and temperature
    degree_days = "degree_days"
    ambient_temperature = "ambient_temperature"

    # Indoor temperature for the building (e.g., HGT 20/12)
    base_temperature = 20.0

    # Heating threshold, heating is required when avg temp is below 12°C
    heating_threshold = 12.0
    # ------------------------------------------------#

    # Functions
    # Calculate target date (yesterday's date)
    target_date = datetime.now() - timedelta(days=1)
    target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)

    # Fetch weather data for the target date
    data = Daily(location, start=target_date, end=target_date)
    data = data.fetch()

    # Check if weather data is available
    if data.empty:
        raise Exception("No weather data available for the specified date.")

    # Extract average temperature
    avg_temp = data["tavg"].iloc[0]

    if avg_temp is None or pd.isnull(avg_temp):
        raise Exception("Average temperature data is missing.")

    # Calculate heating degree days (HDD) if avg_temp is below the heating threshold
    if avg_temp < heating_threshold:
        hdd = base_temperature - avg_temp
    else:
        hdd = 0

    # Round HDD to 2 decimal places
    hdd = round(hdd, 2)

    # Prepare data to be sent
    data = {
        ambient_temperature: avg_temp,
        degree_days: hdd,
    }

    # Send data to Eliona
    eliona.SetHeap(gai, "input", data)
