# Heating Degree Days (HDD) Calculation and Data Submission to Eliona

This script calculates **Heating Degree Days (HDD)** based on weather data for a specified location. It retrieves the previous day average outdoor temperature, computes the required HDD for heating, and sends the results to an asset in the **Eliona** system.
[Detailed information](https://energie.ch/heizgradtage/)

---

## 📋 How the Script Works

1. **Weather Data Fetching**: The script retrieves daily average outdoor temperatures from the [Open-Meteo API](https://open-meteo.com/).
2. **Heating Degree Days Calculation**: HDD is computed based on the difference between a base indoor temperature (20°C) and the outdoor temperature when it falls below the heating threshold (12°C).
3. **Data Submission to Eliona**: The calculated HDD and average outdoor temperature are sent to a specific asset in the Eliona system, identified by its Global Asset Identifier (GAI).

## 🔎 Concept: Heating Degree Days (HDD)

Heating Degree Days (HDD) is a metric used to estimate heating energy requirements for a building. HDD is calculated when the outdoor temperature is below a set threshold (in this case, 12°C). The difference between the base indoor temperature (20°C) and the outdoor temperature shows how much energy is needed to heat the building.

### 📌 Example:
- If the outdoor temperature is **5°C**, the HDD is:
HDD = 20°C - 5°C = 15
- If the outdoor temperature is **14°C**, no heating is needed, and HDD is:
HDD = 0

---

## 🛠️ Variables Explained

Here’s a detailed explanation of the key variables used in the script. These values can be adjusted based on your specific requirements.

### **Location Data**
- **`latitude`**: The latitude of the location where you want to fetch temperature and HDD data.
  - **Default**: `47.499882`
  - **Description**: Represents the latitude coordinate of the location you are monitoring. This can be modified to reflect a different location.
  
- **`longitude`**: The longitude of the location where you want to fetch temperature and HDD data.
  - **Default**: `8.726160`
  - **Description**: Represents the longitude coordinate of the location you are monitoring. This can be modified to reflect a different location.

### **Global Asset Identifier (GAI)**
- **`gai`**: The Global Asset Identifier used in the Eliona system to identify the asset where the data will be sent.
  - **Default**: `"YourGAI"`
  - **Description**: This should be replaced with the actual GAI for the asset in Eliona where you want to store the heating degree days (HDD) and outside temperature data. Make sure that the specified asset exists in the Eliona system.

### **Attribute Names**
- **`degree_days`**: The attribute name in the asset where the calculated heating degree days (HDD) will be stored.
  - **Default**: `"your_degree_days_attribute_name"`
  - **Description**: This is the placeholder for the attribute in the Eliona system where the HDD Default will be recorded. Ensure that this attribute exists in the defined asset, or change it to match your setup.
  
- **`outside_temperature`**: The attribute name in the asset where the fetched outside temperature will be stored.
  - **Default**: `"your_outside_temperature_attribute_name"`
  - **Description**: This attribute stores the average outside temperature fetched from the weather data. Ensure this attribute exists in the defined asset, or adjust it as per your configuration.

### **Temperature Thresholds**
- **`base_temperature`**: The desired indoor temperature, typically set to **20°C**.
  - **Default**: `20.0`
  - **Description**: This is the indoor temperature to which the building should be heated. It is used in the calculation of heating degree days (HDD).

- **`heating_threshold`**: The outdoor temperature threshold, set to **12°C**, below which heating is required.
  - **Default**: `12.0`
  - **Description**: This represents the threshold outdoor temperature. Heating degree days are only calculated if the outdoor temperature falls below this value.

### **Time Configuration**
- **utc_offset_hours**: The UTC offset used to adjust the target date and time.
  - **Default**: `2`
  - **Description**: Defines the number of hours to offset from Coordinated Universal Time (UTC). For example, for UTC+2, set `utc_offset_hours` to `2`. This ensures that the target date is calculated based on the specified time zone, allowing accurate retrieval of temperature and HDD data relative to your local time.

---

## ⚙️ Usage Notes

- The script calculates **Heating Degree Days (HDD)** only when the outdoor temperature is below the threshold set in the **`heating_threshold`** variable (default is 12°C). Ensure the threshold is set according to your heating requirements.

- The timestamp added to the heap is set to 23:59 of the previous day by default. However, this can be modified if necessary in line 39.

- The attributes (`degree_days`, `outside_temperature`) should be of the subtype **"input"** in the Eliona system to ensure the data is correctly stored and processed.

- **Daily Script Execution**: The script retrieves the HDD for the previous day. For optimal performance:
  - Schedule the script to run **daily**. 
  - Add a **small delay** to allow the day to complete before fetching the previous day's data.
  [Eliona documentation about sceduling the script](https://doc.eliona.io/collection/dokumentation/engineering/skript-engine/skripte-konfigurieren)

- **Data Aggregation for HDD**:
  - For the **`degree_days`** attribute, ensure the **aggregation** type is set to **sum**.
  - Select the **month** and **year** options in the aggregation settings so that you can retrieve the **monthly** and **yearly** HDD values easily through the Eliona system.
  [Eliona documentation about Aggregation](https://doc.eliona.io/collection/dokumentation/engineering/asset-modellierung-templates#aggregation)

  
---

## 🔗 API Reference

The script relies on the [Open-Meteo API](https://open-meteo.com/) to retrieve weather data. The following endpoint is used:
https://api.open-meteo.com/v1/forecast
Parameters include:
- `latitude`: Latitude of the location
- `longitude`: Longitude of the location
- `daily`: Fetches daily mean temperature
- `timezone`: Sets the timezone to UTC
