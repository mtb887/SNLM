import json
import os
import hashlib
import traceback
from datetime import datetime

# Directory setup
DATA_DIR = "Data"
INGESTED_DIR = "Ingested_Data"
RAW_DIR = os.path.join(INGESTED_DIR, "raw_protected_Data")
LOG_DIR = "Log_Files"
LOG_FILE = os.path.join(LOG_DIR, "instagram_ingestion_errors.log")

# Ensure required directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INGESTED_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Utility functions
def hash_string(value):
    return hashlib.sha256(value.encode()).hexdigest()

def generate_unique_id(caption, timestamp):
    key = f"{caption}_{timestamp}"
    return hashlib.sha256(key.encode()).hexdigest()

def ingest_instagram():
    try:
        input_path = os.path.join(DATA_DIR, "instagram_data.json")
        output_path = os.path.join(INGESTED_DIR, "instagram_insurance_data.json")
        raw_path = os.path.join(RAW_DIR, "instagram_raw_data.json")

        # Load input
        with open(input_path, "r") as infile:
            posts = json.load(infile)
        print(f"Loaded {len(posts)} Instagram posts")

        seen_ids = set()
        insurance_posts = []

        for post in posts:
            caption = post.get("caption", "")
            if "insurance" in caption.lower():
                timestamp = post.get("timestamp", "NA")
                uid = generate_unique_id(caption, timestamp)

                if uid in seen_ids:
                    continue  # Skip duplicate
                seen_ids.add(uid)

                sanitized = {
                    "unique_id": uid,
                    "id": post.get("id"),
                    "timestamp": timestamp,
                    "caption": caption,
                    "media_type": post.get("media_type"),
                    "media_url": post.get("media_url"),
                    "username_hashed": hash_string(post.get("username", "")) if post.get("username") else None,
                    "comments_count": post.get("comments_count"),
                    "like_count": post.get("like_count")
                }
                insurance_posts.append(sanitized)

        # Save raw
        with open(raw_path, "w") as f:
            json.dump(posts, f)

        # Save sanitized
        with open(output_path, "w") as f:
            json.dump(insurance_posts, f, indent=2)

        print(f"Instagram: {len(insurance_posts)} unique insurance-related posts ingested and sanitized.")

    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"\n[{datetime.now()}] ❌ Error in Instagram ingestion:\n")
            log.write(traceback.format_exc())
        print(f"❌ Error occurred! Check log file at {LOG_FILE}")

if __name__ == "__main__":
    ingest_instagram()
    print("Ingestion complete.")
# Compare this snippet from Ingestion_Scripts/Ingest_facebook.py:
#     # Save raw data 