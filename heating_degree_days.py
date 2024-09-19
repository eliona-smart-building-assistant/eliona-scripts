def UserFunction(id, eliona):
    import urllib.request
    import urllib.parse
    import json
    from datetime import datetime, timedelta, timezone

    try:
        # Variables
        # ------------------------------------------------#
        # Latitude & Longitude of the location
        latitude = 47.499882
        longitude = 8.726160

        # GAI of the Asset where the data should go
        gai = "YourGAI"

        # Attribute names for degree days and temperature
        degree_days = "your_degree_days_attribute_name"
        outside_temperature = "your_outside_temperature_attribute_name"

        # Indoor temperature for the building (e.g., HGT 20/12)
        base_temperature = 20.0

        # Heating threshold, heating is required when avg temp is below 12°C
        heating_threshold = 12.0

        # Define the UTC offset of your timezone. For UTC+2, set utc_offset_hours to 2
        utc_offset_hours = 2
        # ------------------------------------------------#

        # Calculate target date (yesterday's date in UTC)
        utc_offset = timezone(timedelta(hours=utc_offset_hours))
        target_datetime = datetime.now(utc_offset)
        target_date = target_datetime - timedelta(days=1)
        target_date_str = target_date.date().isoformat()

        # Set the timestamp that will be put into the heap to 23:59 of the previous day
        target_date_input = target_date.replace(
            hour=23, minute=59, second=0, microsecond=0
        ).isoformat()

        # Open-Meteo API endpoint
        api_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": target_date_str,
            "end_date": target_date_str,
            "daily": "temperature_2m_mean",
            "timezone": "UTC",
        }

        # Build the URL with parameters
        query_string = urllib.parse.urlencode(params)
        url = f"{api_url}?{query_string}"

        # Fetch data
        try:
            with urllib.request.urlopen(url) as response:
                response_data = response.read()
                data = json.loads(response_data)
        except urllib.error.HTTPError as e:
            error_message = f"HTTP Error: {e.code} - {e.reason}"
            print(error_message, flush=True)
            return
        except urllib.error.URLError as e:
            error_message = f"URL Error: {e.reason}"
            print(error_message, flush=True)
            return
        except Exception as e:
            error_message = f"Unexpected error during data fetch: {e}"
            print(error_message, flush=True)
            return

        # Check if data is available
        if (
            "daily" not in data
            or "temperature_2m_mean" not in data["daily"]
            or not data["daily"]["temperature_2m_mean"]
        ):
            error_message = "No weather data available for the specified date."
            print(error_message, flush=True)
            return

        # Extract average temperature
        avg_temp = data["daily"]["temperature_2m_mean"][0]

        if avg_temp is None:
            error_message = "Average temperature data is missing."
            print(error_message, flush=True)
            return

        # Calculate heating degree days (HDD)
        if avg_temp < heating_threshold:
            hdd = base_temperature - avg_temp
        else:
            hdd = 0

        # Round values
        hdd = round(hdd, 2)
        avg_temp = round(avg_temp, 2)

        # Prepare data to send
        data_to_send = {
            outside_temperature: avg_temp,
            degree_days: hdd,
        }

        # Convert data_to_send to JSON string
        data_json = json.dumps(data_to_send)

        # Prepare SQL INSERT statement
        subtype = "input"  # You can adjust this as needed

        # Ensure that single quotes in JSON are escaped
        data_json_escaped = data_json.replace("'", "''")
        asset_id = eliona.GetAssetIDByGAI(gai)

        # Construct the SQL query with ts, asset_id, subtype, data
        sql_query = f"""
            UPDATE heap
            SET
                ts = '{target_date_input}',
                data = '{data_json_escaped}'
            WHERE
                asset_id = {asset_id}
                AND subtype = '{subtype}';
        """

        # Execute SQL Query to insert data into heap
        try:
            eliona.SQLQuery(query=sql_query)
            print("Data inserted into Eliona heap successfully.", flush=True)
        except Exception as e:
            error_message = f"Error executing SQL query to insert data: {e}"
            print(error_message, flush=True)
            return

    except Exception as e:
        # Catch-all for any other unexpected errors
        print(f"An unexpected error occurred: {e}", flush=True)
        print("E:", e, flush=True)
        return
