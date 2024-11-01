def UserFunction(id, eliona):
    # Main function to count the states of tickets and tasks associated with a specific asset.
    # Steps:
    # 1. Define the asset ID to analyze and the GAI to store the results.
    # 2. Execute an SQL query to retrieve state and parent_id for each ticket associated with the asset.
    # 3. Separate tickets and tasks based on `parent_id` and count occurrences of each state.
    # 4. Prepare data to update the asset heap with ticket and task state counts.
    # 5. Write the updated state counts to the Eliona heap.

    import collections  # Import collections for counting occurrences of each state

    # --- Configuration Variables ---
    # Specify the asset ID from which to collect ticket data.
    asset_id = 1  # Replace with the asset ID you want to analyze

    # Specify the GAI of the asset where the ticket and task state counts should be written.
    gai = (
        "target_asset_GAI"  # Replace with the GAI of the target asset for data storage
    )

    # --- Step 1: Retrieve and Process Ticket Data ---
    # SQL query to fetch state and parent_id for tickets linked to the specified asset.
    query = f"""
    SELECT state, parent_id 
    FROM ticket 
    WHERE asset_id = {asset_id} AND state IS NOT NULL;
    """

    # Execute the SQL query to fetch ticket data for the specified asset.
    ticket_data = eliona.SQLQuery(query)
    print(
        "Ticket data retrieved:", ticket_data, flush=True
    )  # Debug: Output retrieved ticket data

    # Initialize counters to count occurrences of each state for tickets and tasks.
    ticket_state_counts = (
        collections.Counter()
    )  # Counts states for tickets (entries without `parent_id`)
    task_state_counts = (
        collections.Counter()
    )  # Counts states for tasks (entries with `parent_id`)

    # --- Step 2: Separate and Count States for Tickets and Tasks ---
    # Loop through each row in `ticket_data` to classify entries as tickets or tasks.
    for state, parent_id in ticket_data:
        if parent_id is None:
            # If `parent_id` is None, it's a ticket; increment the count in `ticket_state_counts`.
            ticket_state_counts[state] += 1
        else:
            # If `parent_id` is present, it's a task; increment the count in `task_state_counts`.
            task_state_counts[state] += 1

    print(
        "Ticket state counts:", ticket_state_counts, flush=True
    )  # Debug: Output ticket state counts
    print(
        "Task state counts:", task_state_counts, flush=True
    )  # Debug: Output task state counts

    # --- Step 3: Prepare Data for Heap Update ---
    # Prepare a dictionary with the counts of each state for both tickets and tasks.
    update_data = {}

    # Add ticket state counts with a "ticket_" prefix for heap organization.
    for state, count in ticket_state_counts.items():
        update_data[f"ticket_{state}"] = count

    # Add task state counts with a "task_" prefix for heap organization.
    for state, count in task_state_counts.items():
        update_data[f"task_{state}"] = count

    print(
        "Data to update in heap:", update_data, flush=True
    )  # Debug: Output the prepared update data

    # --- Step 4: Update the Asset Heap ---
    # Write the ticket and task state counts to the Eliona heap for the specified GAI.
    eliona.SetHeap(gai, "input", update_data, eliona.MakeSource(id))
