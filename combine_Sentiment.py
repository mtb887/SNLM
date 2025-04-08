import os
import pandas as pd
from datetime import datetime

def combine_sentiment_outputs():
    """
    Combines all daily sentiment parquet files into a single unified file.
    Output path: Processed_Data/YYYY/MM/DD/combined_sentiment.parquet
    """

    # Get today's date
    today = datetime.today()
    year = str(today.year)
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)

    # Build file path
    BASE_DIR = os.path.join("Processed_Data", year, month, day)
    OUTPUT_FILE = os.path.join(BASE_DIR, "combined_sentiment.parquet")

    # Platform files
    platform_files = [
        "twitter_sentiment.parquet",
        "facebook_sentiment.parquet",
        "instagram_sentiment.parquet",
        "linkedin_sentiment.parquet"
    ]

    combined_df = pd.DataFrame()

    for file_name in platform_files:
        file_path = os.path.join(BASE_DIR, file_name)
        if os.path.exists(file_path):
            df = pd.read_parquet(file_path)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            print(f"✅ Loaded {file_name} with {len(df)} records")
        else:
            print(f"⚠️ Skipping {file_name} (not found)")

    if not combined_df.empty:
        combined_df.to_parquet(OUTPUT_FILE, index=False)
        print(f"📦 Combined sentiment data saved to: {OUTPUT_FILE}")
    else:
        print("⚠️ No data to combine — all platform files missing or empty.")
