# 📩 JotForm to Eliona Data Integration and Notification Script

This script automates the process of integrating data from **JotForm** submissions into the **Eliona** system. It fetches the latest submissions from a specified JotForm form, extracts numeric values and comments, updates Eliona assets with this data, and sends an email with an attachment if new data is detected and an attachment is uploaded.

---

## 📋 How the Script Works

1. **Data Retrieval from JotForm**: Connects to the JotForm API to fetch the latest submissions and uploaded files from a specified form.

2. **Data Extraction**: Extracts specific numeric fields and a comment field from the submissions based on predefined field mappings.

3. **Data Comparison**: Compares the new data with existing data in Eliona to identify any changes.

4. **Eliona Data Update**: If changes are detected, updates the specified Eliona assets with the new numeric values and comment.

5. **File Processing and Email Notification**:
   - Checks for the latest uploaded file in JotForm.
   - If the file hasn't been processed before, downloads it, sends it via email to specified recipients, and marks it as processed.

6. **Tracking Processed Files**: Maintains a record of processed files to prevent duplicate processing.

---

## 🛠️ Setup Instructions

### 1. JotForm API Keys

You need two API keys from JotForm:

- **`JOTFORM_API_KEY`**: For fetching submissions data.
- **`JOTFORM_API_KEY_DOWNLOAD`**: For downloading uploaded files.

[How to get your JotForm API key](https://www.jotform.com/help/253-how-to-get-api-key)

Replace the placeholders in the script:

```python
    JOTFORM_API_KEY = "YOUR_JOTFORM_API_KEY"  # Your JotForm API key
    JOTFORM_API_KEY_DOWNLOAD = "YOUR_JOTFORM_API_KEY_FOR_DOWNLOAD"  # JotForm API key for file downloads
```

### 2. JotForm Form ID

Specify the **Form ID** of your JotForm form:

```python
    FORM_ID = "YOUR_FORM_ID"  # The ID of your JotForm form
```

### 3. Eliona API Key and Host

Obtain an API Key from the Eliona platform to authenticate the script.

[How to create an API Key in Eliona](https://doc.eliona.io/collection/dokumentation/einstellungen/api-schlussel#api-schlussel-erstellen)

Replace the placeholders:

```python
    ELIONA_API_KEY = "YOUR_ELIONA_API_KEY"  # Your Eliona API key
    ELIONA_HOST = "https://your.eliona.host/api/v2"  # Your Eliona host URL
```

### 4. Asset Configuration

Specify the **Asset IDs** and **Attribute Names**
```python
    ASSET_ID = 1234  # The asset ID where numeric data will be written
    ASSET_ID_COMMENT = 5678  # The asset ID where comments will be written
    ATTRIBUTE_COMMENT = "your_attribute_comment_name"  # The attribute name for comments
```

Ensure that these assets and attributes exist in Eliona and that the attribute names match the corresponding JotForm fields.

### 5. Fields to Track

Define the **fields to track** from JotForm submissions:

```python
    fields_to_track = [
        "Field 1",
        "Field 2",
        "Field 3",
    ]  # Replace with your actual field names
```

Update `field_mappings` accordingly:

```python
    field_mappings = {
        "numeric_fields": {"type": "control_number", "fields": fields_to_track},
        "comment_field": {"type": "control_textarea", "name": "your_comment_field_name"},
    }

- **`control_number`**: The field type for numeric fields in JotForm.
- **`control_textarea`**: The field type for text area (comments) in JotForm.
- **`name`**: The unique name of the comment field in your JotForm form.
```

**Important**: Ensure that the attribute names in the Eliona asset where the numeric data is written match the names of the corresponding JotForm fields.

### 6. Email Configuration

Set up the email recipients and message:

```python
    email_recipients = [
        "recipient1@example.com",
        "recipient2@example.com",
    ]  # Replace with actual email addresses
    email_subject = "Explanation of Value Deviation"  # Subject of the email
    email_txt_before_message = "The explanation for the deviation is:"  # Text before the message in the email
    email_txt_after_message = "Attached is the explanation as a PDF."  # Text after the message in the email
    file_name_for_email = "ValueDeviationExplanation.pdf"  # The name of the file to be sent via email
```

### 7. File Tracking

Specify the filename for tracking processed files:

```python
    TRACKED_FILE = "processed_pdfs.txt"
```

Typically, this can be left as is.

---

## 🛠️ How to Run the Script

1. **Customize Variables**: Modify the configuration variables as per the instructions above.

2. **Copy to Script Engine**: Upload the script to the Eliona Script Engine.

3. **Schedule Execution**: Configure the script to run periodically (e.g., every minute) to process new submissions. **Note**: Consider the number of API calls allowed per day to avoid exceeding limits; running every minute might result in too many API calls in a day.

4. **Monitor Results in Eliona**: Check the specified assets in Eliona to see the updated data.

5. **Check Email Notifications**: Ensure that emails are being sent to the specified recipients when new data is processed and an attachment is uploaded.


---

## ⚠️ Important Considerations

- **Field Names in JotForm**: Ensure that the `name` attributes of the fields in JotForm match those specified in `field_mappings`. The `name` is different from the label; it's a unique identifier in JotForm.

- **Asset and Attribute Setup**: The assets and attributes in Eliona must be correctly set up to receive the data. Attributes should have the correct subtypes (`input` or `output`) as specified.

- **Email Configuration**: The Eliona system must be configured to send emails, and the email recipients must be valid. Ensure that SMTP settings are correctly configured in Eliona.

- **Data Types**: The script assumes numeric fields can be converted to `float`. Ensure that the data entered in JotForm is compatible.

- **API Limits**: Be aware of any rate limits imposed by the JotForm API to avoid exceeding them during frequent script executions.

---

## 👀 Example Use Case

Imagine you have a JotForm form where users submit meter readings and comments regarding deviations in energy consumption. This script automates the process by:

- **Extracting Submitted Readings and Comments**: Retrieves the latest numeric values and comments from the form submissions.

- **Updating Eliona Assets**: Updates specified assets in Eliona with the new data, ensuring real-time data synchronization.

- **Processing Uploaded Files**: Downloads the latest uploaded file (e.g., a PDF explanation of deviations) and sends it via email to concerned parties.

- **Sending Email Notifications**: Automatically notifies stakeholders when new data is processed, including any attached explanations.

This automation streamlines data management and ensures that all relevant information is up-to-date and communicated effectively.

---

## 🔗 Resources

- **JotForm API Documentation**: [https://api.jotform.com/docs/](https://api.jotform.com/docs/)
- **Eliona API Documentation**: [https://doc.eliona.io/](https://doc.eliona.io/)
- **Eliona Platform**: [https://eliona.io](https://eliona.io)

---

## 📝 Notes

- **Testing**: Before deploying the script in a production environment, test it with a sample form and assets to ensure it works as expected.

- **Error Handling**: The script includes basic error handling, but you may want to enhance it to cover additional edge cases or log errors more comprehensively.

- **Security**: Keep your API keys secure. Do not expose them in public repositories or share them with unauthorized individuals.

- **Customization**: Feel free to customize the script further to meet your specific requirements, such as processing additional fields or integrating with other systems.

---

By following this guide, you'll be able to set up and run the script effectively, integrating your JotForm data into Eliona and automating notifications.
