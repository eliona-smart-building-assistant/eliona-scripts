# Heating Degree Days (HDD) Calculation and Data Submission to Eliona

This script calculates **Heating Degree Days (HDD)** based on weather data for a specified location. It retrieves the daily average outdoor temperature, computes the required HDD for heating, and sends the results to an asset in the **Eliona** system.

## How the Script Works

1. **Weather Data Fetching**: The script retrieves daily average outdoor temperatures from the [Open-Meteo API](https://open-meteo.com/).
2. **Heating Degree Days Calculation**: HDD is computed based on the difference between a base indoor temperature (20°C) and the outdoor temperature when it falls below the heating threshold (12°C).
3. **Data Submission to Eliona**: The calculated HDD and average outdoor temperature are sent to a specific asset in the Eliona system, identified by its Global Asset Identifier (GAI).

## Concept: Heating Degree Days (HDD)

Heating Degree Days (HDD) are a metric used to estimate heating energy requirements for a building. HDD is calculated when the outdoor temperature is below a set threshold (in this case, 12°C). The difference between the base indoor temperature (20°C) and the outdoor temperature indicates how much energy is needed to heat the building.

For example:
- If the outdoor temperature is **5°C**, the HDD is:
HDD = 20°C - 5°C = 15
- If the outdoor temperature is **14°C**, no heating is needed, and HDD is:
HDD = 0

---

## Variables Explained

### **Location Data**
- **`latitude`**: Latitude of the location where temperature data is fetched.
- **Value**: `47.5767`
- **Example**: The latitude for Basel, Switzerland.

- **`longitude`**: Longitude of the location where temperature data is fetched.
- **Value**: `7.5801`
- **Example**: The longitude for Basel, Switzerland.

### **Global Asset Identifier (GAI)**
- **`gai`**: Global Asset Identifier used in the Eliona system to specify the asset where data will be sent.
- **Value**: `"WSJ-Test-HGT"`
- **Purpose**: Identifies the target asset in the Eliona system where the HDD and temperature data will be stored.

### **Attributes**
- **`degree_days`**: The attribute name in the asset for storing the calculated heating degree days (HDD).
- **Purpose**: This specifies where the calculated HDD will be recorded in Eliona.

- **`ambient_temperature`**: The attribute name in the asset for storing the fetched outdoor temperature.
- **Purpose**: This specifies where the average outdoor temperature will be recorded in Eliona.

### **Temperature Thresholds**
- **`base_temperature`**: The base indoor temperature, typically set to **20°C**.
- **Value**: `20.0`
- **Purpose**: Represents the indoor temperature for which the building is heated. Used for HDD calculations.

- **`heating_threshold`**: The outdoor temperature threshold, set to **12°C**, below which heating is required.
- **Value**: `12.0`
- **Purpose**: Heating degree days are calculated only if the outdoor temperature falls below this value.

---

## Script Functionality

### **1. Fetching Weather Data**
The script uses the Open-Meteo API to fetch the daily average outdoor temperature for a specified date and location. It queries the following API:
https://api.open-meteo.com/v1/forecast
The parameters used include latitude, longitude, date, and the UTC timezone.

### **2. Calculating Heating Degree Days (HDD)**
If the daily average outdoor temperature is below the **heating threshold (12°C)**, the HDD is calculated as:
HDD = base_temperature - average_outdoor_temperature
If the outdoor temperature is higher than or equal to the threshold, **no heating is required**, and HDD is set to `0`.

### **3. Sending Data to Eliona**
Once the average outdoor temperature and the HDD have been calculated, they are sent to the Eliona system using the following function:
```python
eliona.SetHeap(gai, "input", data_to_send, eliona.MakeSource(id))
Where gai is the identifier of the asset in Eliona, and data_to_send contains the temperature and HDD data.

Example Calculation
Here is an example for calculating HDD:

Date	Outdoor Temperature	Heating Degree Days	Calculation
01.01.2023	2°C	18	(20 - 2) = 18
02.01.2023	-4°C	24	(20 - (-4)) = 24
03.01.2023	14°C	0	No heating required (14 > 12), HDD = 0
Summary:
Indoor temperature: 20°C
Heating threshold: 12°C
HDD calculation: If outdoor temperature < 12°C, HDD = 20 - outdoor temperature; otherwise, HDD = 0.
Notes
The HDD is calculated for yesterday's date, using UTC timezone.
The base indoor temperature is 20°C, and the heating threshold is 12°C.
Data is fetched from the Open-Meteo API and sent to Eliona for asset tracking and further analysis.

### **Explanation of the Format:**
- **Headers**: Use markdown `#` for main headers and `##` for subheaders, making it easy to read and navigate.
- **Code Blocks**: Code snippets and examples are enclosed in triple backticks (` ``` `) for proper formatting.
- **Tables**: Used for clearly presenting examples, such as the HDD calculations.
- **Bold Text**: Important terms are highlighted with double asterisks (`**`) for emphasis.

This format will ensure that your `README.md` file is well-structured, informative, and easy to read.
