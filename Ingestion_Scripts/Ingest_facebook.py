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
LOG_FILE = os.path.join(LOG_DIR, "facebook_ingestion_errors.log")

# Ensure output directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INGESTED_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Utility functions
def hash_string(value):
    return hashlib.sha256(value.encode()).hexdigest()

def generate_unique_id(message, created_time):
    key = f"{message}_{created_time}"
    return hashlib.sha256(key.encode()).hexdigest()

def ingest_facebook():
    try:
        input_path = os.path.join(DATA_DIR, "facebook_Data.json")
        output_path = os.path.join(INGESTED_DIR, "facebook_insurance_Data.json")
        raw_path = os.path.join(RAW_DIR, "facebook_raw_Data.json")

        # Load data
        with open(input_path, "r") as infile:
            posts = json.load(infile)
        print(f"Loaded {len(posts)} Facebook posts")

        seen_ids = set()
        insurance_posts = []

        for post in posts:
            message = post.get("message", "")
            if "insurance" in message.lower():
                created = post.get("created_time", "NA")
                uid = generate_unique_id(message, created)

                if uid in seen_ids:
                    continue  # skip duplicates
                seen_ids.add(uid)

                user = post.get("from", {})
                sanitized = {
                    "unique_id": uid,
                    "id": post.get("id"),
                    "created_time": created,
                    "message": message,
                    "user": {
                        "id": user.get("id"),
                        "name_hashed": hash_string(user.get("name", "")) if user.get("name") else None
                    },
                    "reactions": post.get("reactions", {}),
                    "comments": post.get("comments", {})
                }
                insurance_posts.append(sanitized)

        # Save raw data (with PII)
        with open(raw_path, "w") as f:
            json.dump(posts, f)

        # Save cleaned, deduplicated output
        with open(output_path, "w") as f:
            json.dump(insurance_posts, f, indent=2)

        print(f"Facebook: {len(insurance_posts)} unique insurance-related posts ingested and sanitized.")

    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"\n[{datetime.now()}] ❌ Error in Facebook ingestion:\n")
            log.write(traceback.format_exc())
        print(f"❌ Error occurred! Check log file at {LOG_FILE}")

if __name__ == "__main__":
    ingest_facebook()
    print("Ingestion complete.")
    print("Check the Ingested_Data folder for the output files.")
    print("Check the Log_Files folder for any errors.")     