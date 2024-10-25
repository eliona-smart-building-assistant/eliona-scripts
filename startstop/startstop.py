import csv
from eliona.api_client2 import ApiClient, Configuration, DataApi
from eliona.api_client2.models.data import Data

import pytz
from datetime import datetime, timedelta, timezone

ELIONA_API_KEY = "FOKlCIwXDNPvI6Ng9CHoOjlZvCypQYZA"  # Replace with your Eliona API key
ELIONA_HOST = (
    "https://experimental.eliona.io/api/v2"  # Replace with your Eliona host URL
)
asset_id = 439  # Replace with the asset ID to monitor
at_range = range(-5, 41)
mt_range = range(8, 27)
table_update_weight = 0.1
table_initial_value = 300
# Define global variables for data
FIELDS = {
    "Wärmepumpe_status": None,
    "heizen_gestartet": None,
    "AT_to_set": None,
    "MT_to_set": None,
    "KonfortZeitEnde": None,
    "Aussentemperatur": None,
    "Massentemperatur": None,
    "KonfortZeit": None,
}
csv_file_path = "temperature_minutes_data.csv"

# Define the timezone for Berlin
berlin_tz = pytz.timezone("Europe/Berlin")

# Configure and authenticate with the Eliona API
configuration = Configuration(host=ELIONA_HOST, api_key={"ApiKeyAuth": ELIONA_API_KEY})
api_client = ApiClient(configuration)
data_api = DataApi(api_client)


def get_datetime_with_time(time_int, timezone):
    time_str = f"{time_int:04}"  # Formats the integer to a 4-character string with zero padding
    today = datetime.now().date()  # Get today's date without timezone info
    naive_datetime = datetime.combine(today, datetime.strptime(time_str, "%H%M").time())
    localized_datetime = timezone.localize(naive_datetime)
    return localized_datetime


def initialize_csv():
    try:
        with open(csv_file_path, mode="r") as csvfile:
            print(f"CSV file {csv_file_path} read successfully.", flush=True)
    except FileNotFoundError:
        table_data = [
            {"AT": at, **{f"MT{idx}": table_initial_value for idx in mt_range}}
            for at in at_range
        ]
        headers = ["AT"] + [f"MT{idx}" for idx in mt_range]
        with open(csv_file_path, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(table_data)
        print(f"CSV file created as {csv_file_path} with default values.", flush=True)


def get_initial_data(fields):
    data_fields = fields.copy()
    data = data_api.get_data(asset_id=asset_id)
    for item in data:
        data_dict = item.data
        for key in data_fields.keys():
            if key in data_dict:
                data_fields[key] = data_dict[key]
    return tuple(data_fields[key] for key in fields.keys())


def check_if_past_comfort_time_end(comfort_time_end):
    now = datetime.now(berlin_tz)
    comfort_time_end_dt = get_datetime_with_time(comfort_time_end, berlin_tz)
    if now > comfort_time_end_dt:
        status_data = Data(
            asset_id=asset_id,
            subtype="output",
            data={"heat_pump_status": 0},
        )
        try:
            data_api.put_data(status_data, direct_mode="true")
            print(
                f"heat_pump_status set to 0 as it is past comfort_time_end {comfort_time_end_dt.strftime('%H:%M')}.",
                flush=True,
            )
        except Exception as e:
            print(f"Exception when updating heat_pump_status to 0: {e}", flush=True)
        exit()


def temperature_hit_target_zero_write_to_csv():
    print("heating_started", heating_started)
    heating_started_datetime = get_datetime_with_time(heating_started, berlin_tz)
    from_date = heating_started_datetime.isoformat()
    print(f"Checking for Temperatur_hit_target hitting 0 after {from_date} ")

    # Fetch data trends to check when Temperatur_hit_target first hit 0
    trends = data_api.get_data_trends(
        from_date=from_date,
        asset_id=asset_id,
        data_subtype="input",
    )

    for trend in trends:
        if trend.data.get("Temperatur_hit_target") == 0:
            target_hit_time = trend.timestamp.astimezone(berlin_tz)
            elapsed_minutes = int(
                (target_hit_time - heating_started_datetime).total_seconds() / 60
            )
            mass_temp_set = f"MT{mass_temp_to_set}"

            def update_csv(outdoor_temp, mass_temp_column, new_elapsed_minutes):
                print(
                    f"Updating CSV at {outdoor_temp}, {mass_temp_column} with 10% weighted average of new value."
                )
                try:
                    rows = []
                    with open(csv_file_path, mode="r") as csvfile:
                        reader = csv.DictReader(csvfile)
                        headers = reader.fieldnames
                        for row in reader:
                            if int(row["AT"]) == outdoor_temp:
                                current_value = int(
                                    row.get(mass_temp_column, table_initial_value)
                                )
                                # Apply a 10% weighted average update
                                updated_value = int(
                                    current_value * (1 - table_update_weight)
                                    + new_elapsed_minutes * table_update_weight
                                )
                                row[mass_temp_column] = updated_value
                            rows.append(row)
                    with open(csv_file_path, mode="w", newline="") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=headers)
                        writer.writeheader()
                        writer.writerows(rows)
                except FileNotFoundError:
                    print(f"File {csv_file_path} does not exist.", flush=True)

            update_csv(outdoor_temp_to_set, mass_temp_set, elapsed_minutes)
            print(
                f"Updated CSV with 10% weighted average of elapsed time ({elapsed_minutes} minutes) at {outdoor_temp_to_set}, {mass_temp_set}.",
                flush=True,
            )
            break  # Stop after finding the first instance
    else:
        print("Temperatur_hit_target did not reach 0. No entry made.", flush=True)


def is_heating_on(heat_pump_status):
    return heat_pump_status == 1


def read_value_in_csv(outdoor_temp, mass_temp_column):
    try:
        with open(csv_file_path, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["AT"]) == outdoor_temp:
                    return int(row.get(mass_temp_column, 0))
        return None
    except FileNotFoundError:
        print(f"File {csv_file_path} does not exist.", flush=True)
        return None


def minutes_until_comfort_time(comfort_time):
    try:
        comfort_dt = get_datetime_with_time(comfort_time, berlin_tz)
        now = datetime.now(berlin_tz)
        if comfort_dt < now:
            comfort_dt += timedelta(days=1)
        return int((comfort_dt - now).total_seconds() / 60)
    except ValueError:
        print("Invalid comfort_time format.", flush=True)
        return None


def start_heating_save_variables():
    current_time_formatted = int(datetime.now(berlin_tz).strftime("%H%M"))
    selected_positions = [0, 1, 2, 3]
    selected_keys = [list(FIELDS.keys())[i] for i in selected_positions]
    status_data = Data(
        asset_id=asset_id,
        subtype="output",
        data={
            selected_keys[0]: 1,
            selected_keys[1]: current_time_formatted,
            selected_keys[2]: outdoor_temperature,
            selected_keys[3]: mass_temperature,
        },
    )
    try:
        data_api.put_data(status_data, direct_mode="true")
        print(
            f"heat_pump_status set to 1 and heating_started set to {current_time_formatted} for asset {asset_id}.",
            flush=True,
        )
    except Exception as e:
        print(
            f"Exception when updating heat_pump_status and heating_started: {e}",
            flush=True,
        )


initialize_csv()

(
    current_heat_pump_status,
    heating_started,
    outdoor_temp_to_set,
    mass_temp_to_set,
    comfort_time_end,
    outdoor_temperature,
    mass_temperature,
    comfort_time,
) = get_initial_data(FIELDS)

check_if_past_comfort_time_end(comfort_time_end)

if is_heating_on(current_heat_pump_status):
    temperature_hit_target_zero_write_to_csv()
else:
    mass_temp_column = f"MT{mass_temperature}"
    table_entry = read_value_in_csv(outdoor_temperature, mass_temp_column)
    minutes_until_comfort = minutes_until_comfort_time(comfort_time)
    time_difference = minutes_until_comfort - table_entry
    print(f"Minutes until comfort_time: {minutes_until_comfort}")
    print(f"Table entry value: {table_entry}")
    print(f"Difference (minutes until comfort_time - table entry): {time_difference}")

    if time_difference < 0:
        start_heating_save_variables()
