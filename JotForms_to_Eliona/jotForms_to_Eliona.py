def UserFunction(id, eliona):
    # Main function that integrates data from JotForm into Eliona and sends emails if necessary.
    # Steps:
    # 1. Import necessary libraries and modules.
    # 2. Define configuration variables (generalized).
    # 3. Define helper functions to fetch and process data.
    # 4. Fetch submissions from JotForm and compare with Eliona data.
    # 5. Update Eliona data and send emails if there are changes.

    import requests
    from eliona.api_client2 import ApiClient, Configuration, DataApi, CommunicationApi
    from eliona.api_client2.models import Data, Message, Attachment
    import base64

    # Configuration Variables
    # Replace the placeholders with your actual configuration values.
    # ------------------------------------------------#
    JOTFORM_API_KEY = "YOUR_JOTFORM_API_KEY"  # Your JotForm API key
    JOTFORM_API_KEY_DOWNLOAD = (
        "YOUR_JOTFORM_API_KEY_FOR_DOWNLOAD"  # JotForm API key for file downloads
    )
    FORM_ID = "YOUR_FORM_ID"  # The ID of your JotForm form
    ELIONA_API_KEY = "YOUR_ELIONA_API_KEY"  # Your Eliona API key
    ELIONA_HOST = "https://your.eliona.host/api/v2"  # Your Eliona host URL
    ASSET_ID = 1234  # The asset ID where data will be written
    ASSET_ID_COMMENT = 5678  # The asset ID for comments to be written on
    ATTRIBUTE_COMMENT = "your_attribute_comment_name"  # The attribute name for comments to be written on
    TRACKED_FILE = "processed_pdfs.txt"  # File to keep track of processed PDFs
    file_name_for_email = "ValueDeviationExplanation.pdf"  # Local filename for the downloaded file that will be send via email
    write_to_subtype = "output"  # Data subtype for numeric values
    write_string_subtype = "input"  # Data subtype for string values
    fields_to_track = [
        "Field 1",
        "Field 2",
        "Field 3",
    ]  # List of fields to track from JotForm submissions
    field_mappings = {
        "numeric_fields": {"type": "control_number", "fields": fields_to_track},
        "comment_field": {"type": "control_textarea", "name": "commentsYou"},
    }
    email_recipients = [
        "recipient1@example.com",
        "recipient2@example.com",
    ]  # List of email recipients
    email_subject = "Explanation of Value Deviation"  # Subject of the email
    email_txt_before_message = (
        "The explanation for the deviation is:"  # Text before the message in the email
    )
    email_txt_after_message = (
        "Attached is the explanation as a PDF."  # Text after the message in the email
    )
    # ------------------------------------------------#

    # Function to get existing data from Eliona for a specific asset
    def get_eliona_data(api_client, asset_id):
        data_api = DataApi(api_client)
        data_entries = data_api.get_data(asset_id, data_subtype=write_to_subtype)
        if data_entries:
            latest_data = max(data_entries, key=lambda x: x.timestamp)
            return latest_data.data
        return {}

    # Function to fetch submissions data from JotForm
    def fetch_jotform_data(api_key, form_id):
        url = f"https://eu-api.jotform.com/form/{form_id}/submissions?apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("content", [])
        return []

    # Function to fetch the latest uploaded file URL from JotForm
    def fetch_latest_uploaded_file(api_key, form_id):
        url = f"https://eu-api.jotform.com/form/{form_id}/files?apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            files = response.json().get("content", [])
            if files:
                latest_file = max(files, key=lambda x: x["date"])
                return latest_file["url"]
        return None

    # Function to download a file from a URL and save it locally
    def download_file(eliona, file_url, local_filename):
        response = requests.get(file_url)
        if response.status_code == 200:
            with eliona.OpenFile(local_filename, "wb") as f:
                f.write(response.content)

    # Function to write numeric data values to Eliona
    def write_to_eliona(api_client, asset_id, data_values):
        data_api = DataApi(api_client)
        data = Data(
            asset_id=asset_id,
            subtype=write_to_subtype,
            data={key: float(value) for key, value in data_values.items()},
        )
        data_api.put_data(data, direct_mode="true")

    # Function to write a string value to Eliona
    def write_string_to_eliona(api_client, asset_id, data_key, data_value):
        if data_value and isinstance(data_value, str):
            data_api = DataApi(api_client)
            data = Data(
                asset_id=asset_id,
                subtype=write_string_subtype,
                data={data_key: data_value},
            )
            data_api.put_data(data, direct_mode="true")

    # Function to send an email with an attachment
    def send_email(api_client, file_path, message):
        communication_api = CommunicationApi(api_client)
        with eliona.OpenFile(file_path, "rb") as f:
            encoded_content = base64.b64encode(f.read()).decode("utf-8")
        attachment = Attachment(
            name=file_path,
            content=encoded_content,
            content_type="application/pdf",
            encoding="base64",
        )
        email_message = Message(
            recipients=email_recipients,
            subject=email_subject,
            content=f"""
                <html>
                <body>
                <p>{email_txt_before_message}<br>
                "{message}"<br>
                {email_txt_after_message}
                </p>
                </body>
                </html>
            """,
            attachments=[attachment],
        )
        response = communication_api.post_mail(email_message)
        print(f"Email sent successfully. Response: {response}")

    # Function to check if a file URL has already been processed
    def has_been_processed(eliona, file_url):
        try:
            with eliona.OpenFile(TRACKED_FILE, "r+") as f:
                processed_files = f.read().splitlines()
                if file_url in processed_files:
                    return True
                else:
                    f.write(f"{file_url}\n")
                    return False
        except FileNotFoundError:
            with eliona.OpenFile(TRACKED_FILE, "w") as f:
                f.write(f"{file_url}\n")
            return False

    # Function to mark a file as processed
    def mark_as_processed(eliona, filename):
        with eliona.OpenFile(TRACKED_FILE, "a") as f:
            f.write(f"{filename}\n")

    # Set up Eliona API client configuration
    configuration = Configuration(
        host=ELIONA_HOST, api_key={"ApiKeyAuth": ELIONA_API_KEY}
    )
    api_client = ApiClient(configuration)

    # Initialize dictionaries to hold last and new values
    last_values = {field: None for field in fields_to_track}
    new_values = {field: None for field in fields_to_track}
    last_comment = None

    # Fetch submissions from JotForm
    submissions = fetch_jotform_data(JOTFORM_API_KEY, FORM_ID)

    # Process submissions to extract new values and the latest comment
    for submission in reversed(submissions):
        answers = submission["answers"]
        # Extract numeric field values
        for field in field_mappings["numeric_fields"]["fields"]:
            for answer in answers.values():
                if (
                    answer["type"] == field_mappings["numeric_fields"]["type"]
                    and answer["name"] == field.lower().replace(" ", "")
                    and "answer" in answer
                ):
                    new_values[field] = answer["answer"]
        # Extract comment field
        for answer in answers.values():
            if (
                answer["type"] == field_mappings["comment_field"]["type"]
                and answer["name"] == field_mappings["comment_field"]["name"]
                and "answer" in answer
            ):
                last_comment = answer["answer"]

    # Get existing data from Eliona
    eliona_existing_data = get_eliona_data(api_client, ASSET_ID)

    # Identify changed values
    changed_values = {
        field: new_value
        for field, new_value in new_values.items()
        if new_value
        and (
            field not in eliona_existing_data
            or eliona_existing_data[field] != float(new_value)
        )
    }

    # If there are changed values, update Eliona and send email if necessary
    if changed_values:
        # Write numeric data to Eliona
        write_to_eliona(api_client, ASSET_ID, changed_values)
        # Write the comment to Eliona
        write_string_to_eliona(
            api_client, ASSET_ID_COMMENT, ATTRIBUTE_COMMENT, last_comment
        )
        # Fetch the latest uploaded file URL from JotForm
        latest_file_url = fetch_latest_uploaded_file(JOTFORM_API_KEY_DOWNLOAD, FORM_ID)
        if latest_file_url:

            # Check if the file_url has already been processed
            if not has_been_processed(eliona, latest_file_url):
                # Download the file
                download_file(eliona, latest_file_url, file_name_for_email)
                # Send an email with the attachment
                send_email(api_client, file_name_for_email, last_comment)
                # Mark the file_url as processed
                mark_as_processed(eliona, latest_file_url)
        # Update the last values
        last_values.update(changed_values)
