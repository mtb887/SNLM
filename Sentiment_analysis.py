import os
import json
from datetime import datetime
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# VADER setup
analyzer = SentimentIntensityAnalyzer()

# Date-based folder structure
today = datetime.today()
year = str(today.year)
month = str(today.month).zfill(2)
day = str(today.day).zfill(2)

BASE_PROCESSED_DIR = os.path.join("Processed_Data", year, month, day)
os.makedirs(BASE_PROCESSED_DIR, exist_ok=True)

# Platform config
platforms = {
    "twitter": {
        "input": "twitter_insurance_data.json",
        "text_key": "text",
        "timestamp_key": "created_at"
    },
    "facebook": {
        "input": "facebook_insurance_data.json",
        "text_key": "message",
        "timestamp_key": "created_time"
    },
    "instagram": {
        "input": "instagram_insurance_data.json",
        "text_key": "caption",
        "timestamp_key": "timestamp"
    },
    "linkedin": {
        "input": "linkedin_insurance_data.json",
        "text_key": "text",
        "timestamp_key": "created.time"
    }
}

INGESTED_DIR = "Ingested_Data"

def classify_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive", score
    elif score <= -0.05:
        return "negative", score
    else:
        return "neutral", score

def run_sentiment_pipeline():
    for platform, config in platforms.items():
        input_path = os.path.join(INGESTED_DIR, config["input"])
        output_path = os.path.join(BASE_PROCESSED_DIR, f"{platform}_sentiment.parquet")

        if not os.path.exists(input_path):
            print(f"Skipping {platform}: file not found.")
            continue

        with open(input_path, "r") as infile:
            records = json.load(infile)

        processed = []
        for record in records:
            text = record.get(config["text_key"], "")
            if not text:
                continue

            sentiment, score = classify_sentiment(text)

            processed.append({
                "unique_id": record.get("unique_id", record.get("id")),
                "platform": platform,
                "text": text,
                "timestamp": record.get(config["timestamp_key"]),
                "sentiment": sentiment,
                "score": round(score, 4)
            })

        df = pd.DataFrame(processed)
        df.to_parquet(output_path, index=False)
        print(f"✅ {platform.capitalize()}: {len(df)} posts saved to {output_path}")

if __name__ == "__main__":
    run_sentiment_pipeline()
    print("Sentiment analysis pipeline completed.")
          