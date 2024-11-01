# 📊 Eliona Ticket and Task State Counter Script

This script counts the states of **tickets** and **tasks** associated with a specified asset in the Eliona system. It organizes these state counts and stores them in Eliona’s heap, enabling tracking of ticket and task statuses for monitoring and analysis.

## 📝 How the Script Works

1. **Configuration**:
   - Specify the **Asset ID** to analyze and the **Global Asset Identifier (GAI)** for storing results.
2. **Data Retrieval**:
   - Run an SQL query to get the state and `parent_id` for each ticket related to the asset.
3. **Classification and Counting**:
   - Separate tickets (entries without a `parent_id`) and tasks (entries with a `parent_id`), then count each unique state for both tickets and tasks.
4. **Heap Update**:
   - Prepare data with ticket and task counts, then store this information in Eliona’s heap with structured attribute names.

---

## 📋 Setup Instructions

### 1. Asset Setup in Eliona

- Create an asset with the following **attributes** to hold the counts of each state for tickets and tasks:
  - **Ticket States**:
    - `ticket_in-progress`
    - `ticket_closed`
    - `ticket_canceled`
    - `ticket_assigned`
    - `ticket_completed`
  - **Task States**:
    - `task_in-progress`
    - `task_closed`
    - `task_canceled`
    - `task_assigned`
    - `task_completed`

Each attribute should have a **subtype** of `"input"` to allow the script to store data in Eliona correctly.

### 2. Configuration Variables

In the script, adjust the following variables as needed:

```python
# Specify the Asset ID you want to analyze
asset_id = 1  # Replace with the desired Asset ID

# Define the Global Asset Identifier (GAI) where state counts should be written
gai = "target_asset_GAI"  # Replace with the GAI for data storage
```

---

## 🛠️ How to Run the Script

1. **Configure Variables**: Customize the `asset_id` and `gai` variables to specify the asset to analyze and the GAI where data will be stored.
2. **Upload to Script Engine**: Add the script to the Eliona Script Engine.
3. **Set a Periodic Schedule**: Schedule the script to run periodically to keep ticket and task counts up to date.
4. **View Results in Eliona**: State counts for tickets and tasks will be available in Eliona under the specified asset attributes, enabling tracking and analysis.

---

## 👀 Example Use Case

This script is useful for teams managing customer support tickets or project tasks. By periodically tracking the states of tickets and tasks, management can gain insights into workloads, identify bottlenecks, and track progress across various states.

---

## 🔗 Resources

- [Eliona API Documentation](https://doc.eliona.io/)
- [Eliona Platform](https://eliona.io)

Ensure that assets and attributes in Eliona are correctly set up as described to enable the script to function properly and store accurate results.
