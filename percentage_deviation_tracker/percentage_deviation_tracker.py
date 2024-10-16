def UserFunction(id, eliona):
    from eliona.api_client2 import ApiClient, Configuration, DataApi
    from datetime import datetime, timedelta, timezone

    # Variables for the asset and API configuration.
    # These should be customized for general use.
    # ------------------------------------------------#
    source_asset_id = 1  # Replace with the asset ID to monitor
    target_gai = "your_target_GAI_here"  # Replace with the GAI of the target asset
    days_back = 1000  # Number of days to fetch data for
    ELIONA_API_KEY = "your_api_key_here"  # Replace with your Eliona API key
    ELIONA_HOST = "https://your.url.io//api/v2"  # Replace with your Eliona host URL
    # ------------------------------------------------#

    # Configure and authenticate with the Eliona API.
    # This section creates a connection using your API key and host URL.
    configuration = Configuration(
        host=ELIONA_HOST, api_key={"ApiKeyAuth": ELIONA_API_KEY}
    )

    # Retrieve data trends for the specified asset.
    # This section fetches historical data from the source asset for the past 'days_back' days.
    with ApiClient(configuration) as api_client:
        data_api = DataApi(api_client)
        from_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        data = data_api.get_data_trends(
            asset_id=source_asset_id, from_date=from_date.isoformat()
        )
        data_dicts = [
            d.data for d in data
        ]  # Store fetched data in a list of dictionaries

    # Process the fetched data to organize attribute values over time.
    # This step groups all values by their attribute keys.
    attributes = {}
    for data_dict in data_dicts:
        for key, value in data_dict.items():
            if key not in attributes:
                attributes[key] = []
            attributes[key].append(value)

    # Calculate the plausibility of changes in attribute values over time.
    # This step calculates the average difference between unique values and computes a "plausibility score."
    plausibilitaet = {}
    for key, values in attributes.items():
        values = [float(v) for v in values]  # Ensure all values are numerical
        unique_values = []
        prev_value = None
        summe = 0

        # Track unique differences between consecutive values.
        for value in values:
            if value != prev_value:
                if prev_value is not None:
                    unique_values.append(value - prev_value)
                    summe += value - prev_value
                prev_value = value

        # Calculate the average difference and the plausibility percentage.
        if len(unique_values) != 0:
            average_difference = summe / len(unique_values)
            plausibilitaet[key] = (average_difference / unique_values[-1]) * 100

    # Submit the calculated plausibility data to Eliona.
    # This step writes the results into the heap of the target asset.
    eliona.SetHeap(target_gai, "input", plausibilitaet, eliona.MakeSource(id))
