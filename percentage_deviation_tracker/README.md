# ⚡ Eliona Percentage Deviation Tracker Script

This script tracks the plausibility of changes in the values of attributes over time within the Eliona system. By calculating how much the current value deviates from the average difference between previous values, it helps monitor the usage patterns. This is particularly useful for electricity meters or other **cumulative counters**, enabling you to detect unusual usage patterns and take action if values deviate too far from the average.

## 📝 How the Script Works
- **Data Fetching:** Retrieves attribute values from a source asset over a user-defined period (default: 1000 days).
- **Plausibility Calculation:** For each attribute, the script calculates the percentage deviation of the most recent value from the average difference between previous values.
- **Data Submission:** The calculated plausibility percentage is submitted to a target asset identified by its Global Asset Identifier (GAI).
- **Monitoring:** The percentage deviation can be used to monitor plausibility, trigger alarms if the deviation exceeds a threshold (e.g., 30%), or track energy usage patterns over time.

---

## 📋 Setup Instructions

### 1. Eliona API Key

You need an API Key from the Eliona platform to authenticate the script. 
[How to create an API Key](https://doc.eliona.io/collection/dokumentation/einstellungen/api-schlussel#api-schlussel-erstellen)
Replace the placeholder with your API key:

ELIONA_API_KEY = "your_api_key_here"

### 2. Source Asset ID

Identify the **Asset ID** of the source asset you want to monitor.

Replace the `source_asset_id` in the script:

source_asset_id = 1  # Replace with the asset ID you want to monitor

### 3. Target Asset GAI

Create a target asset in the Eliona platform with the same asset type as the source asset. Then, obtain the **Global Asset Identifier (GAI)** for the target asset.

Replace the placeholder with the target GAI:

target_gai = "your_target_GAI_here"

### 4. API Host URL

Set the appropriate **Eliona Host URL** for your environment:

ELIONA_HOST = "https://your.url.io//api/v2"

### 5. Time Period

You can adjust the time period (in days) to monitor changes by modifying the `days_back` variable:

days_back = 1000  # The number of days to check for changes

### 6. Monitoring Other Attribute Subtypes
By default, the script can monitor any attribute subtype, such as **input** or **output**. However, it can only write the calculated results into attributes with the input subtype.

If you want to monitor **output** attributes (or other subtypes), follow these steps:

- **Create a new asset type** that has the same attributes as the source asset, but with the attributes set to **input** instead of **output**. [How to create an Asset Type](https://doc.eliona.io/collection/dokumentation/assets/asset-modellierung-templates-erstellen/ein-neues-template-erstellen)
- Ensure that the **target** asset (with the GAI) uses this new asset type, where the relevant attributes are configured as **input**.
This ensures the script can track changes for any attribute type but submit results to attributes designated as **input**.

---

## 🛠️ How to Run the Script

1. **Customize the Variables:** Modify the API key, asset IDs, and other variables as instructed above.
2. **Copy the Script to the Script Engine:** Once customized, copy the script to the Eliona Script Engine.
3. **Schedule Daily Runs:** Configure the script to run daily (or as needed) to track changes over time.
4. **Monitor Results in Eliona:** The plausibility percentage will be displayed for each attribute in the target asset, allowing you to track deviations and identify potential issues.

---

## 👀 Example Use Case

### Monitoring Energy Usage

For example, if you are tracking electricity counters in a building, this script will help you understand if the current consumption is significantly different from the typical usage pattern. If the deviation exceeds a certain threshold (e.g., 30%), you can set up alerts to notify you of potential issues, such as unusual power consumption or inefficiencies.

### Detecting Anomalies

In addition to energy monitoring, the script could be used to track changes in other cumulative counters or attributes. If the plausibility percentage shows an unusual deviation, it could indicate a need for investigation or action, ensuring more reliable and efficient system management.

---

## 🔗 Resources

- [Eliona API Documentation](https://doc.eliona.io/)
- [Eliona Platform](https://eliona.io)

Make sure your assets and attributes are properly configured in Eliona to ensure the script functions correctly and displays accurate results.
