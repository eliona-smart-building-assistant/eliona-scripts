# Heating Degree Days (HDD) Calculation and Data Submission to Eliona

This script calculates **Heating Degree Days (HDD)** based on weather data for a specified location. It retrieves the daily average outdoor temperature, computes the required HDD for heating, and sends the results to an asset in the **Eliona** system.

---

## 📋 How the Script Works

1. **Weather Data Fetching**: The script retrieves daily average outdoor temperatures from the [Open-Meteo API](https://open-meteo.com/).
2. **Heating Degree Days Calculation**: HDD is computed based on the difference between a base indoor temperature (20°C) and the outdoor temperature when it falls below the heating threshold (12°C).
3. **Data Submission to Eliona**: The calculated HDD and average outdoor temperature are sent to a specific asset in the Eliona system, identified by its Global Asset Identifier (GAI).

---

## 🔎 Concept: Heating Degree Days (HDD)

Heating Degree Days (HDD) is a metric used to estimate heating energy requirements for a building. HDD is calculated when the outdoor temperature is below a set threshold (in this case, 12°C). The difference between the base indoor temperature (20°C) and the outdoor temperature shows how much energy is needed to heat the building.

### 📌 Example:
- If the outdoor temperature is **5°C**, the HDD is:
HDD = 20°C - 5°C = 15
- If the outdoor temperature is **14°C**, no heating is needed, and HDD is:
HDD = 0

---

## 🛠️ Variables Explained

These are the key variables you can modify to fit your specific requirements.

### **Location Data**
- **`latitude`**: The latitude of the location where you want to get temperature and HDD data from.
- Default: `47.5767`
- **`longitude`**: The longitude of the location where you want to get temperature and HDD data from.
- Default: `7.5801`

### **Global Asset Identifier (GAI)**
- **`gai`**: Global Asset Identifier used in the Eliona system to specify the asset where the data will be sent.
- Default: `"WSJ-Test-HGT"`
- **Important**: Ensure that your asset in Eliona has the correct GAI or update the script accordingly.

### **Attributes**
- **`degree_days`**: The attribute name in the asset for storing the calculated heating degree days (HDD).
- **Note**: Make sure the attributes of the given asset GAI match this value in your Eliona system.

- **`ambient_temperature`**: The attribute name in the asset for storing the fetched outdoor temperature.
- **Purpose**: Specifies where the average outdoor temperature will be recorded in Eliona.
- **Note**: Ensure that the asset GAI in your Eliona system has attributes corresponding to this name.

---

### **Temperature Thresholds**
- **`base_temperature`**: The base indoor temperature, typically set to **20°C**.
- **Purpose**: Represents the desired indoor temperature for heating. Used to calculate HDD.

- **`heating_threshold`**: The outdoor temperature threshold, set to **12°C**, below which heating is required.
- **Purpose**: HDD is only calculated if the outdoor temperature is below this value.

---

## ⚙️ Usage Notes

- The script fetches **yesterday's temperature data** using the **UTC timezone**.
- It is essential to ensure the asset in Eliona with the GAI defined in the script has the appropriate attribute names (`degree_days`, `ambient_temperature`).
- The script calculates **HDD** only when the outdoor temperature is below the threshold of **12°C**.

---

## 💡 Customization

You can adjust the following parameters based on your specific needs:
- Modify the **latitude** and **longitude** to fetch weather data from a different location.
- Adjust the **base temperature** or **heating threshold** as needed for different heating requirements.
- Ensure the **GAI** and **attribute names** in Eliona match the ones in this script for proper data submission.

---

## 🔗 API Reference

The script relies on the [Open-Meteo API](https://open-meteo.com/) to retrieve weather data. The following endpoint is used:
https://api.open-meteo.com/v1/forecast
Parameters include:
- `latitude`: Latitude of the location
- `longitude`: Longitude of the location
- `daily`: Fetches daily mean temperature
- `timezone`: Sets the timezone to UTC
