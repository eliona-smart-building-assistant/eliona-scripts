def UserFunction(id, eliona):
    # --- Variable Declarations ---

    # Interval for querying closed tickets (e.g., '5 minutes')
    INTERVAL = "5 minutes"

    # General Attribute Identifier (GAI) for heap storage
    GAI = "Ticket Statistik"

    # Subtype identifier for heap storage
    SUBTYPE = "input"

    # Attribute name for storing the ticket count (in German)
    ATTRIBUTE_NAME = "Geschlossene Tickets in den letzten 5 Minuten"

    # --- Execution ---

    # SQL query to count tickets closed within the specified interval
    query_closed_tickets = (
        "SELECT COUNT(*) AS anzahl "
        "FROM ticket "
        "WHERE parent_id IS NULL "
        f"AND closed_at >= NOW() - INTERVAL '{INTERVAL}';"
    )

    # Execute the SQL query and store the result in closed_tickets
    closed_tickets = eliona.SQLQuery(query_closed_tickets)

    # Output the count of closed tickets to the console for logging purposes
    print("closed tickets in the last", INTERVAL, "=", closed_tickets[0][0], flush=True)

    # Prepare structured data for heap storage with the ticket count
    data_closed_tickets = {ATTRIBUTE_NAME: closed_tickets[0][0]}

    # Store the structured data in Eliona’s heap under the GAI and subtype identifiers
    eliona.SetHeap(GAI, SUBTYPE, data_closed_tickets, eliona.MakeSource(id))
