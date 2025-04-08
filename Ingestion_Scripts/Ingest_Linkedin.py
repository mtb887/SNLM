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
LOG_FILE = os.path.join(LOG_DIR, "linkedin_ingestion_errors.log")

# Create required directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INGESTED_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True) 

def hash_string(value):
    return hashlib.sha256(value.encode()).hexdigest()

def generate_unique_id(text, timestamp):
    key = f"{text}_{timestamp}"
    return hashlib.sha256(key.encode()).hexdigest()

def ingest_linkedin():
    try:
        input_path = os.path.join(DATA_DIR, "linkedin_data.json")
        output_path = os.path.join(INGESTED_DIR, "linkedin_insurance_data.json")
        raw_path = os.path.join(RAW_DIR, "linkedin_raw_data.json")

        # Load data
        with open(input_path, "r") as infile:
            posts = json.load(infile)
        print(f"Loaded {len(posts)} LinkedIn posts")

        seen_ids = set()
        insurance_posts = []

        for post in posts:
            text = post.get("text", {}).get("text", "")
            if "insurance" in text.lower():
                created = post.get("created", {}).get("time", "NA")
                uid = generate_unique_id(text, created)

                if uid in seen_ids:
                    continue  # Skip duplicates
                seen_ids.add(uid)

                author = post.get("author", {})
                sanitized = {
                    "unique_id": uid,
                    "id": post.get("id"),
                    "created": post.get("created"),
                    "text": text,
                    "author": {
                        "id": author.get("id"),
                        "name_hashed": hash_string(author.get("name", "")) if author.get("name") else None
                    },
                    "reactionSummary": post.get("reactionSummary"),
                    "commentSummary": post.get("commentSummary")
                }
                insurance_posts.append(sanitized)

        # Save raw data
        with open(raw_path, "w") as f:
            json.dump(posts, f)

        # Save sanitized, deduplicated data
        with open(output_path, "w") as f:
            json.dump(insurance_posts, f, indent=2)

        print(f"LinkedIn: {len(insurance_posts)} unique insurance-related posts ingested and sanitized.")

    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"\n[{datetime.now()}] ❌ Error in LinkedIn pipeline:\n")
            log.write(traceback.format_exc())
        print(f"❌ Error occurred! Check log file at {LOG_FILE}")

if __name__ == "__main__":
    ingest_linkedin()
    print("Ingestion complete.")
# Ingestion complete.           