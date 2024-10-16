def UserFunction(id, eliona):
    from eliona.api_client2 import ApiClient, Configuration, DataApi
    from datetime import datetime, timedelta, timezone

    # Set variables for the source asset, target asset, and Eliona API configuration.
    # These should be customized according to your needs.
    # ------------------------------------------------#
    source_asset_id = 1  # Replace with the asset ID you want to monitor
    target_gai = "your_target_GAI_here"  # Replace with the target GAI where data will be submitted
    days_back = 30  # The number of days to check for changes
    ELIONA_API_KEY = "your_api_key_here"  # Replace with your Eliona API key
    ELIONA_HOST = "https://your.url.io//api/v2"  # Replace with your Eliona host URL
    # ------------------------------------------------#

    # Configure and authenticate with the Eliona API.
    # This section creates a connection using your API key and host URL.
    configuration = Configuration(
        host=ELIONA_HOST, api_key={"ApiKeyAuth": ELIONA_API_KEY}
    )

    # Use the API client to retrieve data trends for the specified asset.
    # This section fetches the historical data for the last 'days_back' days.
    with ApiClient(configuration) as api_client:
        data_api = DataApi(api_client)
        from_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        data = data_api.get_data_trends(
            asset_id=source_asset_id, from_date=from_date.isoformat()
        )
        data_dicts = [d.data for d in data]  # Store data in a list of dictionaries

    # Process the fetched data to collect attribute values over time.
    # Here, we gather all the values for each attribute across the selected period.
    attributes = {}
    for data_dict in data_dicts:
        for key, value in data_dict.items():
            if key not in attributes:
                attributes[key] = []
            attributes[key].append(value)

    # Calculate the number of unique changes for each attribute.
    # This part checks how many unique values exist for each attribute over the time period.
    number_changes = {}
    for key, values in attributes.items():
        values = [float(v) for v in values]  # Ensure all values are numerical
        unique_values = []  # Store unique values
        prev_value = None
        for value in values:
            if value != prev_value:
                unique_values.append(value)
                prev_value = value
        number_changes[key] = len(unique_values)  # Count unique changes

    # Send the calculated results back to Eliona.
    # This section submits the number of unique changes for each attribute to the target asset in Eliona.
    eliona.SetHeap(target_gai, "input", number_changes, eliona.MakeSource(id))
