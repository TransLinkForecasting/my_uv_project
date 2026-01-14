# TLPyTools Example Project

This project demonstrates how to use the `tlpytools` package to interact with Azure SQL Server and Azure Data Lake Storage (ADLS).

## Overview

The example script (`main.py`) demonstrates:
1. Creating a sample pandas DataFrame
2. Writing data to Azure SQL Server
3. Writing data to Azure Data Lake Storage (ADLS Gen2)
4. Reading data from Azure SQL Server
5. Reading data from Azure Data Lake Storage (ADLS Gen2)

## Prerequisites

### Required Environment Variables

The following environment variables must be present in the `.env` file in your project directory. If it doesn't, refer to `env.examples` and add them:

- **`TLPT_AZURE_SQL_URI`**: Your Azure SQL Server URI (e.g., `yourserver.database.windows.net`)
- **`ORCA_ADLS_URL`**: Your Azure Data Lake Storage URL using the Data Lake Gen2 API endpoint (e.g., `https://yourstorageaccount.dfs.core.windows.net`)

### Azure Authentication

- **Azure SQL**: Uses `ActiveDirectoryInteractive` authentication (browser-based login)
- **ADLS**: Uses `DefaultAzureCredential` (supports multiple authentication methods including Azure CLI, PowerShell, Environment Variables, Managed Identity, etc.)

### Python Dependencies

Install dependencies using:
```bash
pip install -r requirements.txt
```

Or with uv:
```bash
uv pip install -r requirements.txt
```

## Configuration

Edit the global variables in `main.py` to match your environment:

```python
# Azure SQL Server configuration
AZURE_SQL_SCHEMA = "examples"      # Your schema name
AZURE_SQL_TABLE = "example_table"   # Your table name

# ADLS configuration (reads from ORCA_ADLS_URL environment variable)
ADLS_BASE_PATH = f"{os.getenv('ORCA_ADLS_URL')}/dev/uv_example"
LOCAL_TEMP_DIR = "C:/Temp"          # Local temporary directory for file operations
FILE_NAME = "example_data.csv"      # Name of the file to write/read
```

## Running the Example

```bash
python main.py
```

## Important Notes

### ADLS URL Format

The ADLS URL **must** use the Data Lake Storage Gen2 API endpoint:
- ✅ Correct: `https://accountname.dfs.core.windows.net`
- ❌ Incorrect: `https://accountname.blob.core.windows.net`

Using the blob endpoint will result in a `MissingRequiredHeader` error.

### Azure SQL Write Access

If you only have read-only access to Azure SQL Server, comment out the write section (Step 2) in `main.py`:

```python
# 2. Write dataframe to Azure SQL - Comment out this section if you only have read only access
# print("\n2. Writing dataframe to Azure SQL...")
# table_spec = {"example": f"{AZURE_SQL_SCHEMA}.{AZURE_SQL_TABLE}"}
# df_dict = {"example": df}
# azure_td_tables.write_tables(table_spec, df_dict)
# print(f"Written to {AZURE_SQL_SCHEMA}.{AZURE_SQL_TABLE}")
```

## What the Script Does

1. **Creates Sample Data**: Generates a pandas DataFrame with 5 rows containing ID, name, value, and date columns
2. **Writes to Azure SQL**: Uploads the DataFrame to the specified schema and table (creates/replaces the table)
3. **Writes to ADLS**: Saves the DataFrame as a CSV file locally, then uploads it to Azure Data Lake Storage
4. **Reads from Azure SQL**: Retrieves the data back from the SQL table and displays it
5. **Reads from ADLS**: Downloads the CSV file from ADLS and reads it into a DataFrame

## Troubleshooting

### Authentication Issues

- Ensure you're logged in via Azure CLI (`az login`) or Azure PowerShell (`Connect-AzAccount`)
- For ADLS, you may need to configure `DefaultAzureCredential` behavior using environment variables:
  - `OPTION_EXCLUDE_MANAGED_IDENITITY_CREDENTIAL=True`
  - `OPTION_EXCLUDE_INTERACTIVE_BROWSER_CREDENTIAL=False`

### Missing Environment Variables

If environment variables are not set, the script will fail. Ensure both `TLPT_AZURE_SQL_URI` and `ORCA_ADLS_URL` are configured in your environment.

### File Conflicts in ADLS

If a file already exists in ADLS, the `adls_util` will automatically rename the existing file with a timestamp suffix (e.g., `example_data_202601140026_bak.csv`) before uploading the new file.

## Additional Resources

- [tlpytools documentation](https://pypi.org/project/tlpytools/)
- [Azure Data Lake Storage Gen2 documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [Azure SQL Database documentation](https://learn.microsoft.com/en-us/azure/azure-sql/)