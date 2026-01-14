"""
Simple example script demonstrating how to use tlpytools to:
1. Create a sample dataframe
2. Write to Azure SQL Server
3. Write to Azure Data Lake Storage
4. Read from Azure SQL Server
5. Read from Azure Data Lake Storage

Prerequisites:
- Set environment variable TLPT_AZURE_SQL_URI with your Azure SQL server URI
- Configure Azure authentication (DefaultAzureCredential)
"""

import pandas as pd
import os

# Import tlpytools modules - this automatically loads .env files via env_config
from tlpytools.sql_server import azure_td_tables
from tlpytools.adls_server import adls_tables

# Explicitly ensure environment is loaded (belt and suspenders approach)
try:
    from tlpytools.env_config import ensure_env_loaded

    ensure_env_loaded(verbose=True)
except ImportError:
    print("Warning: Could not import env_config, .env file may not be loaded")

# Global configuration
# - table schema and name for Azure SQL Server example (productivity for read, adm2 for read/write)
AZURE_SQL_SCHEMA = "examples"
AZURE_SQL_TABLE = "example_table"
# - path to use for ADLS example (must use adm2 account)
# NOTE: Must use dfs.core.windows.net (Data Lake Gen2 API), not blob.core.windows.net

# Get ADLS URL from environment variable with validation
ORCA_ADLS_URL = os.getenv("ORCA_ADLS_URL")
if not ORCA_ADLS_URL:
    print(
        "DEBUG: Environment variables available:",
        [k for k in os.environ.keys() if "ORCA" in k or "TLPT" in k],
    )
    raise ValueError(
        "Environment variable 'ORCA_ADLS_URL' is not set. "
        "Please set it to your Azure Data Lake Storage URL "
        "(e.g., https://yourstorageaccount.dfs.core.windows.net)"
    )
ADLS_BASE_PATH = f"https://{ORCA_ADLS_URL}/dev/uv_example"
LOCAL_TEMP_DIR = "C:/Temp"
FILE_NAME = "example_data.csv"


def main():
    print("=" * 70)
    print("TLPyTools Simple Example")
    print("=" * 70)

    # 1. Create example dataframe
    print("\n1. Creating example dataframe...")
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "value": [100, 200, 300, 400, 500],
            "date": pd.date_range("2024-01-01", periods=5),
        }
    )
    print(f"Created dataframe with shape: {df.shape}")
    print(df)

    # 2. Write dataframe to Azure SQL - Comment out this section if you only have read only access
    print("\n2. Writing dataframe to Azure SQL...")
    table_spec = {"example": f"{AZURE_SQL_SCHEMA}.{AZURE_SQL_TABLE}"}
    df_dict = {"example": df}
    azure_td_tables.write_tables(table_spec, df_dict)
    print(f"Written to {AZURE_SQL_SCHEMA}.{AZURE_SQL_TABLE}")

    # 3. Write dataframe to ADLS
    print("\n3. Writing dataframe to ADLS...")
    os.makedirs(LOCAL_TEMP_DIR, exist_ok=True)
    df.to_csv(os.path.join(LOCAL_TEMP_DIR, FILE_NAME), index=False)
    adls_uri = f"{ADLS_BASE_PATH}/{FILE_NAME}"
    adls_tables.write_table_by_name(adls_uri, LOCAL_TEMP_DIR, FILE_NAME)
    print(f"Written to {adls_uri}")

    # 4. Read dataframe from Azure SQL
    print("\n4. Reading dataframe from Azure SQL...")
    sql_df_dict = azure_td_tables.read_tables(
        schema=AZURE_SQL_SCHEMA, table=AZURE_SQL_TABLE, source="server"
    )
    sql_df = sql_df_dict[f"{AZURE_SQL_SCHEMA}.{AZURE_SQL_TABLE}"]
    print(f"Read from Azure SQL - shape: {sql_df.shape}")
    print(sql_df)

    # 5. Read dataframe from ADLS
    print("\n5. Reading dataframe from ADLS...")
    file_bytes = adls_tables.get_table_by_name(adls_uri)
    adls_df = pd.read_csv(file_bytes)
    print(f"Read from ADLS - shape: {adls_df.shape}")
    print(adls_df)

    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
