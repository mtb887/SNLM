import json
import os
import hashlib

DATA_DIR = "Data"
INGESTED_DIR = "Ingested_Data"
RAW_DIR = os.path.join(INGESTED_DIR, "raw_protected_Data")

# Ensure output directories exist
os.makedirs(INGESTED_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

def hash_string(value):
    """Simple SHA-256 hashing to pseudonymize usernames."""
    return hashlib.sha256(value.encode()).hexdigest()

def ingest_twitter():
    """Ingests Twitter data, removes/masks PII, and writes sanitized output."""

    input_path = os.path.join(DATA_DIR, "twitter_data.json")
    output_path = os.path.join(INGESTED_DIR, "twitter_insurance_data.json")
    raw_copy_path = os.path.join(RAW_DIR, "twitter_raw_data.json")

    # Load data
    with open(input_path, "r") as infile:
        tweets = json.load(infile)
    print(f"Loaded {len(tweets)} Twitter posts")

    insurance_tweets = []
    for tweet in tweets:
        text = tweet.get("text", "")
        if "insurance" in text.lower():
            user = tweet.get("user", {})
            sanitized = {
                "id": tweet.get("id"),
                "created_at": tweet.get("created_at"),
                "text": text,
                "user": {
                    "id": user.get("id"),  # safe to keep
                    "username_hashed": hash_string(user.get("username", "")) if user.get("username") else None
                },
                "retweet_count": tweet.get("retweet_count"),
                "favorite_count": tweet.get("favorite_count")
            }
            insurance_tweets.append(sanitized)

    # Write full raw data for secure/internal access only
    with open(raw_copy_path, "w") as rawfile:
        json.dump(tweets, rawfile)

    # Write sanitized data
    with open(output_path, "w") as outfile:
        json.dump(insurance_tweets, outfile, indent=2)

    print(f"Ingested and sanitized {len(insurance_tweets)} Twitter posts containing 'insurance'.")
if __name__ == "__main__":
    ingest_twitter()
    print("Ingestion complete.")