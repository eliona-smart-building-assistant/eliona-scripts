
# 📄 PDF Attachment Processor for Eliona

This script processes **PDF attachments** uploaded to an asset in the **Eliona** system. It extracts specific values from the PDFs based on keywords, then submits the extracted data to Eliona as attribute values. The script tracks which attachments have already been processed to avoid duplication.

---

## 📋 How the Script Works

1. **Asset and Attachment Retrieval**: The script connects to the Eliona system, retrieves an asset by its ID, and checks its attachments.
2. **File Keyword Matching**: It processes PDF attachments only if their filename contains a specified keyword.
3. **PDF Value Extraction**: Using predefined keywords, the script extracts corresponding numerical values from the PDF.
4. **Data Submission**: The extracted values are sent to Eliona as attribute data for the asset.
5. **Tracking Processed Attachments**: The script maintains a record of processed files to avoid reprocessing the same attachment.

### ⚠️ Important Considerations:
- **PDF Format**: Only files in `.pdf` format are processed.
- **File Name Keyword**: Ensure that the file name contains the (`file_name_keyword`); otherwise, the file will be skipped.
- **Unique File Names**: Do not upload files with the same name twice, as the script will skip files already processed.
- **Attribute Names**: Ensure that the attribute names in the asset's template match the keywords specified in the script (`value_keywords`). The script extracts values based on these keywords and sends them to the corresponding attributes in Eliona. [Attribute zum Template hinzufügen](https://doc.eliona.io/collection/dokumentation/assets/asset-modellierung-templates-erstellen/ein-neues-template-erstellen#id-3-attribute-zum-template-hinzufugen)

---

## 🛠️ Setup Instructions

### 1. Eliona API Key

You need an API Key from the Eliona platform to authenticate the script. 
[How to create an API Key](https://doc.eliona.io/collection/dokumentation/einstellungen/api-schlussel#api-schlussel-erstellen)
Replace the placeholder with your API key:

```python
ELIONA_API_KEY = "your_api_key_here"
```

### 2. Asset ID

Specify the **Asset ID** of the asset you want to process:

```python
asset_id = 1  # Replace with your asset ID
```

### 3. File Name Keyword

Define the **keyword** to match file names that should be processed:

```python
file_name_keyword = "billing"  # Replace with your file name keyword
```

### 4. Value Extraction Keywords

Specify the **keywords** that the script will search for in the PDF to extract values:

```python
value_keywords = [
    "total amount",
    "total net",
]  # Replace with your keywords
```

These keywords must match the attribute names in the asset's template. Ensure that the attributes in the asset have the same names as the keywords, or the data submission to Eliona will fail.

---

## 🛠️ How to Run the Script

1. **Customize Variables**: Modify the API key, asset ID, file name keyword, and value keywords as needed.
2. **Upload to Script Engine**: Copy the script to the Eliona Script Engine.
3. **Daily/Periodic Execution**: Schedule the script to run periodically to process newly uploaded files.
4. **Monitor Results in Eliona**: Extracted data will be available in the asset's attributes, as defined in the asset's template.

---

## 👀 Example Use Case

Imagine a utility company is uploading **billing PDFs** for an asset (e.g., a building). This script extracts the **"total amount"** and **"total net"** from the PDFs, then sends the values to Eliona for storage and analysis. By ensuring that the file names contain a specific keyword (like "billing") and that the asset attributes are correctly named, the company can easily track and visualize payment data over time.

---

## 🔗 Resources

- [Eliona API Documentation](https://doc.eliona.io/)
- [Eliona Platform](https://eliona.io)

Ensure your asset and attributes are correctly configured in Eliona to allow the script to function properly and display accurate results.
