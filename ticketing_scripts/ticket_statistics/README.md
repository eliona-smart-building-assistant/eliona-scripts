# 📊 Eliona Project Ticket and Task Statistics Script

This script analyzes **tickets** and **tasks** related to a specific project within the Eliona platform. It categorizes tickets by state, priority, reason, and age, while also counting open vs. closed tickets and tasks. The script aggregates this information and stores it in Eliona’s heap, where it can be used for analysis, reporting, and operational oversight.

## 📝 How the Script Works

1. **Configuration**:
   - Define the **Project ID** to analyze and the **Global Asset Identifier (GAI)** for storing results.
2. **Data Retrieval**:
   - Execute SQL queries to retrieve tickets directly related to the project and tasks associated with these tickets.
3. **Data Processing**:
   - For tickets:
     - Count open and closed tickets.
     - Classify tickets by state, priority, reason, and age brackets.
   - For tasks:
     - Count open and closed tasks.
     - Classify tasks by state.
4. **Heap Update**:
   - Prepare data with aggregated counts, then store the results in Eliona’s heap using structured attribute names.

---

## 📋 Setup Instructions

### 1. Asset Setup in Eliona

To use this script, the asset identified by the specified **Global Asset Identifier (GAI)** must have the following **attributes** for the script to store the aggregated data correctly:

- **Ticket and Task Counts**:
  - `Open Tickets`
  - `Closed Tickets`
  - `Open Tasks`
  - `Closed Tasks`

- **Ticket Age Brackets**:
  - `Ticket Age 1 Day`
  - `Ticket Age 3 Days`
  - `Ticket Age 1 Week`
  - `Ticket Age 1 Month`
  - `Ticket Age Over 1 Month`

- **Ticket and Task States**:
  - `Ticket State closed`
  - `Ticket State canceled`
  - `Ticket State assigned`
  - `Ticket State in-progress`
  - `Ticket State completed`
  - `Task State in-progress`
  - `Task State closed`
  - `Task State canceled`
  - `Task State completed`
  - `Task State assigned`

- **Ticket Priority**:
  - `Ticket Priority 0`
  - `Ticket Priority 1`

- **Ticket Reasons**:
  - `Ticket Reason maintenance`
  - `Ticket Reason error`
  - `Ticket Reason service`
  - `Ticket Reason other`
  - `Ticket Reason cleaning`

Each attribute must have a subtype of `"input"` to ensure the script can write data to Eliona correctly.

### 2. Configuration Variables

In the script, adjust the following variables:

```python
# Project ID to analyze
project_id = 1  # Replace with the actual project ID

# Global Asset Identifier (GAI) where data will be stored
gai = "your_gai_here"  # Replace with the target GAI for data storage
```

---

## 🛠️ How to Run the Script

1. **Configure Variables**: Set the `project_id` and `gai` variables to specify the project to analyze and the GAI for data storage.
2. **Deploy to Script Engine**: Upload the script to the Eliona Script Engine.
3. **Schedule for Periodic Execution**: Schedule the script to run periodically, allowing it to update ticket and task statistics regularly.
4. **View Results in Eliona**: Aggregated statistics will be available under the specified attributes in Eliona, providing insights into project-related tickets and tasks.

---

## 👀 Example Use Case

This script is valuable for project management teams to gain insights into tickets and tasks associated with a specific project. By tracking the counts and statuses of tickets and tasks, as well as ticket priorities, reasons, and age brackets, teams can identify trends, manage workloads, and address any backlogs effectively.

---

## 🔗 Resources

- [Eliona API Documentation](https://doc.eliona.io/)
- [Eliona Platform](https://eliona.io)

Ensure that the asset and attributes in Eliona are correctly configured to enable the script to function properly and store accurate results.
