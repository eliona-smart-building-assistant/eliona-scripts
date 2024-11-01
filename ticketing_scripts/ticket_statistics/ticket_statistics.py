def UserFunction(id, eliona):
    # Main function to gather ticket and task statistics for a specific project.
    # Steps:
    # 1. Define configuration variables, including project ID and GAI for data storage.
    # 2. Retrieve tickets and tasks related to the specified project ID using SQL queries.
    # 3. Process tickets to count states, prioritize reasons, and categorize by age.
    # 4. Process tasks to count states and calculate open vs closed status.
    # 5. Prepare and format data for updating the asset heap.
    # 6. Write the formatted data to the Eliona heap.

    import datetime
    from collections import Counter
    from datetime import timedelta

    # --- Configuration Variables ---
    # Define the project ID to analyze.
    project_id = 1  # Replace with the actual project ID for analysis

    # Define the GAI for the asset where the statistics will be written.
    gai = "your_gai_here"  # Replace with the target GAI where data will be submitted

    # --- Step 1: Retrieve Tickets and Tasks Data ---
    # SQL query to retrieve tickets directly related to the project (no parent_id).
    query_tickets = f"""
    SELECT ticket_id, state, priority, reason, created_at, closed_at 
    FROM ticket 
    WHERE parent_id IS NULL AND proj_id = '{project_id}';
    """
    tickets = eliona.SQLQuery(
        query_tickets
    )  # Execute query to fetch tickets for the project

    # SQL query to retrieve tasks indirectly related to the project (linked by parent ticket).
    query_tasks = f"""
    SELECT t.ticket_id, t.state, t.created_at, t.closed_at
    FROM ticket t
    JOIN ticket parent ON t.parent_id = parent.ticket_id
    WHERE parent.proj_id = '{project_id}';
    """
    tasks = eliona.SQLQuery(
        query_tasks
    )  # Execute query to fetch tasks related to the project

    # --- Step 2: Initialize Counters and Variables ---
    # Counters for open/closed tickets and tasks
    open_tickets = 0
    closed_tickets = 0
    open_tasks = 0
    closed_tasks = 0

    # Counters for ticket and task states
    ticket_state_counts = Counter()
    task_state_counts = Counter()

    # Categorization for ticket age brackets
    ticket_age_brackets = {
        "1_day": 0,
        "3_days": 0,
        "1_week": 0,
        "1_month": 0,
        "over_1_month": 0,
    }

    # Counters for ticket priority and reason
    ticket_priority_counts = Counter()
    ticket_reason_counts = Counter()

    # Get the current time to calculate ticket age
    current_time = datetime.datetime.now(datetime.timezone.utc)

    # --- Step 3: Process Tickets ---
    # Loop through each ticket to update counts for state, age, priority, and reason.
    for ticket_id, state, priority, reason, created_at, closed_at in tickets:
        # Count open vs closed tickets
        if state == "closed":
            closed_tickets += 1
        else:
            open_tickets += 1

        # Count tickets by state
        ticket_state_counts[state] += 1

        # Calculate ticket age and categorize into age brackets
        age = (current_time - created_at).days
        if age <= 1:
            ticket_age_brackets["1_day"] += 1
        elif age <= 3:
            ticket_age_brackets["3_days"] += 1
        elif age <= 7:
            ticket_age_brackets["1_week"] += 1
        elif age <= 30:
            ticket_age_brackets["1_month"] += 1
        else:
            ticket_age_brackets["over_1_month"] += 1

        # Count tickets by priority
        ticket_priority_counts[priority] += 1

        # Count tickets by reason if reason is provided
        if reason:
            ticket_reason_counts[reason] += 1

    # --- Step 4: Process Tasks ---
    # Loop through each task to update counts for state and open vs closed status.
    for task_id, state, created_at, closed_at in tasks:
        # Count open vs closed tasks
        if state == "closed":
            closed_tasks += 1
        elif state != "canceled":
            open_tasks += 1

        # Count tasks by state
        task_state_counts[state] += 1

    # --- Step 5: Prepare Data for Heap Update ---
    # Prepare a dictionary to hold the statistics to be updated in the asset heap.
    update_data = {
        "Open Tickets": open_tickets,
        "Closed Tickets": closed_tickets,
        "Ticket Age 1 Day": ticket_age_brackets["1_day"],
        "Ticket Age 3 Days": ticket_age_brackets["3_days"],
        "Ticket Age 1 Week": ticket_age_brackets["1_week"],
        "Ticket Age 1 Month": ticket_age_brackets["1_month"],
        "Ticket Age Over 1 Month": ticket_age_brackets["over_1_month"],
        "Open Tasks": open_tasks,
        "Closed Tasks": closed_tasks,
    }

    # Add ticket state counts to update_data with "Ticket State" prefix
    for state, count in ticket_state_counts.items():
        update_data[f"Ticket State {state}"] = count

    # Add task state counts to update_data with "Task State" prefix
    for state, count in task_state_counts.items():
        update_data[f"Task State {state}"] = count

    # Add ticket priority counts to update_data with "Ticket Priority" prefix
    for priority, count in ticket_priority_counts.items():
        update_data[f"Ticket Priority {priority}"] = count

    # Add ticket reason counts to update_data with "Ticket Reason" prefix
    for reason, count in ticket_reason_counts.items():
        update_data[f"Ticket Reason {reason}"] = count

    print(
        "Data to update in heap:", update_data, flush=True
    )  # Debug: Output the prepared data

    # --- Step 6: Update the Asset Heap ---
    # Write the aggregated data to the Eliona heap for the specified GAI.
    eliona.SetHeap(gai, "input", update_data, eliona.MakeSource(id))
