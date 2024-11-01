# 📊 Eliona Ticket Closure Statistic Script

This script tracks the number of tickets closed within a specified interval and stores this information in Eliona’s heap storage. By monitoring closed tickets over time, you can analyze trends and activity levels, helping with workload management or identifying potential areas for operational improvement.

## 📝 How the Script Works

1. **Configuration**:
   - The script is configured to count tickets closed within a user-defined interval (default: **5 minutes**).
2. **Ticket Count Retrieval**:
   - An SQL query counts the tickets marked as closed within this interval.
3. **Data Storage**:
   - The count of closed tickets is stored in the Eliona heap under a designated attribute, making it accessible for further analysis or visualization.


---

## 📋 Setup Instructions

### 1. Set the Query Interval

Specify the **interval** at which to check for closed tickets. The default is set to `5 minutes`, but this can be adjusted:

```python
INTERVAL = "5 minutes"  # Adjust the interval as needed
```

### 2. Define the Global Asset Identifier (GAI)

Identify the **Global Asset Identifier (GAI)** under which the ticket statistics will be stored in Eliona:

```python
GAI = "Ticket Statistik"  # Update the GAI if needed
```

### 3. Attribute Settings

Define the **subtype** and **attribute name** for storing the ticket count:

```python
SUBTYPE = "input"  # Define the attribute subtype as 'input' for heap storage
ATTRIBUTE_NAME = "Geschlossene Tickets in den letzten 5 Minuten"  # Update attribute name if needed
```

---

## 🛠️ How to Run the Script

1. **Configure Variables**: Adjust the `INTERVAL`, `GAI`, `SUBTYPE`, and `ATTRIBUTE_NAME` variables to suit your requirements.
2. **Deploy to Script Engine**: Upload the script to the Eliona Script Engine.
3. **Schedule for Periodic Execution**: Set the script to run at regular intervals, matching the `INTERVAL` value to ensure all closed tickets are captured within each period.
4. **View Results in Eliona**: The closed ticket data will be accessible in Eliona under the specified asset attributes, as set up in the asset’s template.


---

## 👀 Example Use Case

### Operational Monitoring

This script is particularly useful for monitoring help desk or customer service teams by tracking the number of tickets resolved within specific time frames. By examining trends in ticket closures, management can assess team performance, detect peaks in activity, and adjust resources accordingly.

---

## 🔗 Resources

- [Eliona API Documentation](https://doc.eliona.io/)
- [Eliona Platform](https://eliona.io)

Ensure assets and attributes are correctly set up in Eliona to allow the script to function properly and store accurate results.
