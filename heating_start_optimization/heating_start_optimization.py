def UserFunction(id, eliona):
    # Import necessary modules for API interaction, data handling, and time manipulation.
    import csv
    from eliona.api_client2 import ApiClient, Configuration, DataApi
    from eliona.api_client2.models.data import Data
    import os
    import pytz
    from datetime import datetime, timedelta, time

    # Configuration Variables - Replace these with actual values for deployment.
    # ------------------------------------------------#
    api_key = "YOUR_ELIONA_API_KEY"  # Your Eliona API key
    host = "https://your.eliona.host/api/v2"  # Your Eliona host URL
    asset_id = 439  # ID for the target asset in Eliona
    at_range = range(-5, 41)  # Range of outdoor temperatures for the table
    mt_range = range(8, 27)  # Range of mass temperatures for the table
    tb_up_wght = 0.1  # Weight for table update calculations
    tb_init_val = 300  # Initial table value for mass temperature
    csv_path = "temp_min_data.csv"  # Path for storing CSV data locally
    berlin_tz = pytz.timezone("Europe/Berlin")  # Timezone for Berlin
    FIELDS = {  # Define fields to track specific temperature data
        "Wärmepumpe_status": None,
        "heizen_gestartet": None,
        "AT_to_set": None,
        "MT_to_set": None,
        "KonfortZeitEnde": None,
        "Aussentemperatur": None,
        "Massentemperatur": None,
        "KonfortZeit": None,
        "Temperatur_hit_target": None,
        "Innentemperatur": None,
        "Konforttemperatur": None,
    }
    # ------------------------------------------------#

    # Initialize the Eliona API client.
    configuration = Configuration(host=host, api_key={"ApiKeyAuth": api_key})
    api_client = ApiClient(configuration)
    api = DataApi(api_client)

    # Helper function to create a localized datetime object based on a time integer
    def get_datetime_with_time(time_int, timezone):
        time_str = f"{time_int:04}"
        naive_datetime = datetime.combine(
            datetime.now().date(), time(int(time_str[:2]), int(time_str[2:]))
        )
        return timezone.localize(naive_datetime)

    # Function to initialize a CSV file if it doesn't already exist.
    # This CSV stores data used in temperature calculations.
    def initialize_csv():
        try:
            with eliona.OpenFile(csv_path, mode="r") as csvfile:
                pass  # File exists, no action needed.
        except FileNotFoundError:
            # Create a new CSV with initial values.
            table_data = [
                {"AT": at, **{f"MT{idx}": tb_init_val for idx in mt_range}}
                for at in at_range
            ]
            headers = ["AT"] + [f"MT{idx}" for idx in mt_range]
            with eliona.OpenFile(csv_path, mode="w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(table_data)

    # Fetch initial data values for specific fields from Eliona.
    def get_initial_data(fields):
        data_fields = fields.copy()
        data = api.get_data(asset_id=asset_id)
        for item in data:
            data_dict = item.data
            for key in data_fields.keys():
                if key in data_dict:
                    data_fields[key] = data_dict[key]
        return tuple(data_fields[key] for key in fields.keys())

    # Check if the current time is past the comfort end time.
    # If past, turn off the heat pump by updating its status in Eliona.
    def check_if_past_cf_time_end(cf_time_end):
        now = datetime.now(berlin_tz)
        cf_t_end_dt = get_datetime_with_time(cf_time_end, berlin_tz)
        if now > cf_t_end_dt:
            status_data = Data(
                asset_id=asset_id,
                subtype="output",
                data={"Wärmepumpe_status": 0},
            )
            api.put_data(status_data, direct_mode="true")
            exit()

    # Update the CSV with a new value when the heat pump reaches its target.
    def update_csv(outdoor_temp, mass_temp_column, new_elapsed_minutes):
        outdoor_temp = int(round(outdoor_temp))
        mass_temp_column = f"MT{int(round(mass_temp_column))}"
        rows = []
        with eliona.OpenFile(csv_path, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            for row in reader:
                if int(row["AT"]) == outdoor_temp:
                    current_value = int(row.get(mass_temp_column, tb_init_val))
                    updated_value = int(
                        current_value * (1 - tb_up_wght)
                        + new_elapsed_minutes * tb_up_wght
                    )
                    row[mass_temp_column] = updated_value
                rows.append(row)
        with eliona.OpenFile(csv_path, mode="w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    # Function to log heating activation time in the CSV if the target temperature is reached.
    def temperature_hit_target_zero_write_to_csv():
        heat_start_dt = get_datetime_with_time(heating_started, berlin_tz)
        from_date = heat_start_dt.isoformat()
        today_date = datetime.now(berlin_tz).date()
        timestamp_file = "timestamp.txt"
        if os.path.exists(timestamp_file):
            with eliona.OpenFile(timestamp_file, "r") as file:
                last_timestamp_str = file.read().strip()
                if last_timestamp_str:
                    last_timestamp = datetime.fromisoformat(
                        last_timestamp_str
                    ).astimezone(berlin_tz)
                    if last_timestamp.date() == today_date:
                        return
        trends = api.get_data_trends(
            from_date=from_date,
            asset_id=asset_id,
            data_subtype="input",
        )
        for trend in trends:
            temp_hit_target_string = list(FIELDS.keys())[8]
            if trend.data.get(temp_hit_target_string) == 0:
                target_hit_time = trend.timestamp.astimezone(berlin_tz)
                elapsed_minutes = int(
                    (target_hit_time - heat_start_dt).total_seconds() / 60
                )
                with eliona.OpenFile(timestamp_file, "w") as file:
                    file.write(target_hit_time.isoformat())
                update_csv(at_temp_set, ma_temp_set, elapsed_minutes)
                break

    # Checks if the heat pump is active.
    def is_heating_on(heat_pump_status):
        return heat_pump_status == 1

    # Reads a temperature entry from the CSV based on outdoor and mass temperature.
    def read_value_in_csv(outdoor_temp, mass_temp_column):
        try:
            outdoor_temp = int(round(outdoor_temp))
            mass_temp_column = f"MT{int(round(mass_temp_column))}"
            with eliona.OpenFile(csv_path, mode="r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if int(row["AT"]) == outdoor_temp:
                        return int(row.get(mass_temp_column, 0))
            return None
        except FileNotFoundError:
            return None

    # Calculate minutes until comfort time, adjusting for next day if needed.
    def min_until_ct_time(comfort_time):
        try:
            comfort_dt = get_datetime_with_time(comfort_time, berlin_tz)
            now = datetime.now(berlin_tz)
            if comfort_dt < now:
                comfort_dt += timedelta(days=1)
            return int((comfort_dt - now).total_seconds() / 60)
        except ValueError:
            return None

    # Function to activate heating and save the related variables in Eliona.
    def start_heating_save_variables():
        now = datetime.now(berlin_tz)
        curr_time = now.hour * 100 + now.minute
        selected_positions = [0, 1, 2, 3]
        selected_keys = [list(FIELDS.keys())[i] for i in selected_positions]
        status_data = Data(
            asset_id=asset_id,
            subtype="output",
            data={
                selected_keys[0]: 1,
                selected_keys[1]: curr_time,
                selected_keys[2]: at_temp,
                selected_keys[3]: ma_temperature,
            },
        )
        api.put_data(status_data, direct_mode="true")

    # Initialize CSV file and retrieve initial values from Eliona.
    initialize_csv()
    (
        curr_status,
        heating_started,
        at_temp_set,
        ma_temp_set,
        cf_time_end,
        at_temp,
        ma_temperature,
        comfort_time,
        temperature_hit_target,
        indoor_temp,
        comfort_temp,
    ) = get_initial_data(FIELDS)

    # Check and respond to current heating and temperature statuses.
    check_if_past_cf_time_end(cf_time_end)
    if is_heating_on(curr_status):
        temperature_hit_target_zero_write_to_csv()
    else:
        if indoor_temp >= comfort_temp:
            return
        table_entry = read_value_in_csv(at_temp, ma_temperature)
        min_until_ct = min_until_ct_time(comfort_time)
        time_difference = min_until_ct - table_entry
        if time_difference < 0:
            start_heating_save_variables()
