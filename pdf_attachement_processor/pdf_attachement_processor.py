def UserFunction(id, eliona):
    # Main function orchestrating the overall workflow.
    # 1. Imports necessary libraries and sets up the API client.
    # 2. Checks for an asset using the provided `asset_id` and retrieves its attachments.
    # 3. Processes each attachment, decoding it, extracting values if it's a PDF, and then writing those values to the Eliona API.
    # 4. Skips any attachments that have already been processed.
    # 5. Saves the names of processed attachments to a file for tracking.

    import os, base64, re
    import eliona.api_client2
    from eliona.api_client2.rest import ApiException
    from eliona.api_client2.api.data_api import DataApi
    from eliona.api_client2 import ApiClient, Configuration
    from eliona.api_client2.models.data import Data
    from PyPDF2 import PdfReader

    # Variables
    # These should be customized according to your needs.
    # ------------------------------------------------#
    ELIONA_API_KEY = "your_api_key_here"  # Replace with your Eliona API key
    ELIONA_HOST = "https://your.url.io//api/v2"  # Replace with your Eliona host URL
    asset_id = 1  # Asset ID for the target asset
    file_name_keyword = "billing"  # Keyword to match PDF file names
    value_keywords = [
        "total amount",
        "total net",
    ]  # Keywords for extracting values from the PDF
    # ------------------------------------------------#

    config = Configuration(host=ELIONA_HOST)  # Eliona API host URL
    config.api_key["ApiKeyAuth"] = ELIONA_API_KEY  # Eliona API key
    PROCESSED_ATTACHMENTS_FILE = "/tmp/processed_attachments.txt"

    api_client = ApiClient(config)

    # Initializes an API instance to work with assets.
    assets_api = eliona.api_client2.AssetsApi(api_client)
    # Retrieves the list of attachments that have been processed.
    processed_attachments = read_processed_attachments()

    # Fetches asset info and attachments based on asset_id.
    if asset := get_asset_info_and_attachments(asset_id):
        # Extracts and processes the attachments if they exist.
        attachments = asset.attachments or []
        save_and_process_attachments(
            attachments,
            asset_id,
            file_name_keyword,
            value_keywords,
            processed_attachments,
        )
    else:
        # Prints an error if the asset was not found.
        print(f"Asset with ID {asset_id} not found", flush=True)

    def get_asset_info_and_attachments(asset_id):
        # Fetches asset information along with its attachments based on the asset ID.
        # Returns asset info if successful, or None in case of an exception.
        try:
            return assets_api.get_asset_by_id(
                asset_id=asset_id, expansions=["Asset.attachments"]
            )
        except ApiException as e:
            return None

    def read_processed_attachments():
        # Reads a file containing the names of previously processed attachments.
        # Returns a set of these processed attachment names.
        if os.path.exists(PROCESSED_ATTACHMENTS_FILE):
            with open(PROCESSED_ATTACHMENTS_FILE, "r") as f:
                return set(f.read().splitlines())
        return set()

    def write_processed_attachment(attachment_name):
        # Appends the name of a processed attachment to a file to track which attachments have already been processed.
        with open(PROCESSED_ATTACHMENTS_FILE, "a") as f:
            f.write(f"{attachment_name}\n")

    def save_and_process_attachments(
        attachments, asset_id, file_name_keyword, value_keywords, processed_attachments
    ):
        # Saves each attachment locally and processes it if it meets the required conditions.
        # 1. Checks if the attachment is already processed (by its name).
        # 2. Saves the attachment to a local directory.
        # 3. If it's a PDF and matches the file name keyword, extracts values from the PDF.
        # 4. Writes the extracted values to the Eliona API and records the attachment as processed.

        # Creates a directory to store attachments.
        os.makedirs(f"/tmp/asset_{asset_id}_attachments", exist_ok=True)

        for attachment in attachments:
            # Skips the attachment if it has already been processed.
            if attachment.name in processed_attachments:
                continue

            # Saves the attachment locally.
            file_path = f"/tmp/asset_{asset_id}_attachments/{attachment.name}"
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(attachment.content))

            # If the attachment is a PDF and matches the file name keyword, process it.
            if (
                attachment.name.lower().endswith(".pdf")
                and file_name_keyword.lower() in attachment.name.lower()
            ):
                # Extracts values from the PDF based on specified keywords.
                values = extract_values_from_pdf(file_path, value_keywords)
                if values:
                    # Sends the extracted values to the Eliona API.
                    write_to_eliona(api_client, asset_id, values)
                    # Marks the attachment as processed.
                    write_processed_attachment(attachment.name)

    def extract_values_from_pdf(file_path, keywords):
        # Extracts specific values from a PDF file based on provided keywords.
        # 1. Reads the PDF and extracts its text content.
        # 2. Searches for the keywords in the text and extracts associated numerical values.
        # 3. Returns a dictionary with the keywords and their corresponding values (if found).

        # Opens the PDF file and extracts its text content.
        with open(file_path, "rb") as f:
            text = "".join(page.extract_text() for page in PdfReader(f).pages)

        # Initializes a dictionary to store extracted values.
        values = {}

        # Loops over each keyword and searches for it in the extracted text.
        for keyword in keywords:
            start_index = text.find(keyword)
            if start_index != -1:
                # If the keyword is found, extracts the text following the keyword to locate the value.
                start_index += len(keyword)
                remaining_text = text[start_index:].strip()
                match = re.search(
                    r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?", remaining_text
                )
                if match:
                    # Converts the matched value into a float, replacing commas with periods.
                    value = match.group(0).replace(",", ".")
                    try:
                        values[keyword] = float(value)
                    except ValueError:
                        values[keyword] = None
                else:
                    # If no numerical value is found, stores None for that keyword.
                    values[keyword] = None
            else:
                # If the keyword is not found in the text, stores None for that keyword.
                values[keyword] = None
        return values

    def write_to_eliona(api_client, asset_id, data_values):
        # Sends the extracted data values to the Eliona API for the specified asset.
        # If an error occurs during the API request, it catches the exception and prints an error message.
        try:
            DataApi(api_client).put_data(
                Data(asset_id=asset_id, subtype="input", data=data_values),
                direct_mode="true",
            )
        except ApiException as e:
            print(f"Error writing data: {e}", flush=True)
