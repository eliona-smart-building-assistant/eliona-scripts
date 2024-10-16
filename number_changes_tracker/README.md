# 📊 Eliona Number Of Changes Tracker Script

This script helps track and monitor the number of unique changes occurring in the attributes of a specified asset within the Eliona system. By storing the results in a target asset, it allows for easy visualization and monitoring of attribute changes over a given time period.

## 📝 How the Script Works
- **Data Fetching:** Retrieves attribute values from a source asset over a user-defined period (default: 30 days).
- **Unique Change Calculation:** Counts unique changes in all attributes, ensuring that only actual changes are captured.
- **Data Submission:** Submits the calculated number of changes to a target asset identified by its Global Asset Identifier (GAI).
- **Monitoring:** View the number of changes for each attribute directly within the Eliona platform.

---

## 📋 Setup Instructions

### 1. Eliona API Key

You need an API Key from the Eliona platform to authenticate the script. 
[How to create an API Key](https://doc.eliona.io/collection/dokumentation/einstellungen/api-schlussel#api-schlussel-erstellen)
Replace the placeholder with your API key:

```python
ELIONA_API_KEY = "your_api_key_here"
```
### 2. Source Asset ID

Identify the **Asset ID** of the source asset you want to monitor.

Replace the `source_asset_id` in the script:

```python
source_asset_id = 1  # Replace with the asset ID you want to monitor
```
### 3. Target Asset GAI

Create a target asset in the Eliona platform with the same asset type as the source asset. Then, obtain the **Global Asset Identifier (GAI)** for the target asset.

Replace the placeholder with the target GAI:

```python
target_gai = "your_target_GAI_here"
```
### 4. API Host URL

Set the appropriate **Eliona Host URL** for your environment:

```python
ELIONA_HOST = "https://your.url.io//api/v2"
```
### 5. Time Period

You can adjust the time period (in days) to monitor changes by modifying the `days_back` variable:

```python
days_back = 30  # The number of days to check for changes
```

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
4. **Monitor Results in Eliona:** The number of changes will be displayed for each attribute in the target asset, allowing you to visualize trends over time.

---

## 👀 Example Use Case

Imagine you are monitoring sensor data like **temperature** or **power consumption** in a building. By tracking how often these values change, you can identify **trends**, detect **anomalies**, or recognize **inefficiencies**in building management.

Additionally, it could be used to monitor user-driven changes. For example, if you're tracking how often a specific **configuration or setting** was changed in the past 30 days, you could set a rule to trigger an alarm if the value was changed **more than twice**. This could help in identifying **unintended behavior** or **misuse**, ensuring better control and oversight of critical systems.

---

## 🔗 Resources

- [Eliona API Documentation](https://doc.eliona.io/)
- [Eliona Platform](https://eliona.io)

Make sure that your assets and attributes are correctly set up in Eliona to ensure the script functions properly and displays accurate results.
