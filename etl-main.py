"""
main.py

Main ETL pipeline for earthquake data from USGS API to BigQuery.
Supports both real-time (last 24 hours) and historical daily fetch.

Author: [Bayu]
Created: 2025-07-06
"""

import os
import argparse
import logging
from datetime import datetime

from etl.extract import fetch_earthquake_all_day
from etl.transform import clean_earthquake_data, enrich_earthquake_data
from etl.load import upload_to_bigquery

from prefect import flow

from dotenv import load_dotenv
load_dotenv()

# === Logging Setup ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"etl_log_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

@flow(name="ETL Pipeline", log_prints=True)
def run_pipeline(mode="replace"):
    """
    Run the ETL pipeline with configurable mode.

    Parameters:
        mode (str): 'realtime' or 'historical'
        start_date (str): (for historical) in 'YYYY-MM-DD'
        end_date (str): (for historical) in 'YYYY-MM-DD'
    """

    logging.info(f"Starting ETL pipeline in mode: {mode.upper()}")

    # === 1. Extract ===
    df_raw = fetch_earthquake_all_day()
    
    if df_raw.empty:
        logging.warning("No data fetched. Exiting pipeline.")
        return
    logging.info(f"Extracted {len(df_raw)} rows")

    # === 2. Transform ===
    df_cleaned = clean_earthquake_data(df_raw)
    df_final = enrich_earthquake_data(df_cleaned)
    logging.info(f"Transformed data shape: {df_final.shape}")

    # === 3. Load ===
    try:
        PROJECT_ID = os.getenv("PROJECT_ID")
        TABLE_ID = os.getenv("TABLE_ID")
        CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")

        upload_to_bigquery(
            df=df_final,
            table_id=TABLE_ID,
            project_id=PROJECT_ID,
            credentials_path=CREDENTIALS_PATH,
            if_exists=mode
        )

        logging.info("ETL pipeline completed successfully")
    except Exception as e:
        logging.error(f"ETL pipeline failed {e}")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Run Earthquake ETL Pipeline")
    # parser.add_argument("--mode", type=str, choices=["realtime", "historical"], default="realtime")
    # parser.add_argument("--start_date", type=str, help="Start date (YYYY-MM-DD) for historical mode")
    # parser.add_argument("--end_date", type=str, help="End date (YYYY-MM-DD) for historical mode")

    # args = parser.parse_args()

    # run_pipeline(mode=args.mode, start_date=args.start_date, end_date=args.end_date)

    run_pipeline()
