import json
import random
import os
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Ensure the Data directory exists
DATA_DIR = "Data"
os.makedirs(DATA_DIR, exist_ok=True)

# Random date generator
def random_date():
    return (datetime.now() - timedelta(days=random.randint(0, 30), 
                                       hours=random.randint(0, 23), 
                                       minutes=random.randint(0, 59))).isoformat()

# Insurance-related phrases
insurance_phrases = [
    "Looking for insurance recommendations.",
    "Just claimed my insurance, process was easy!",
    "Anyone know a good health insurance?",
    "Thinking about life insurance, is it worth it?",
    "Car insurance premiums are high this year!",
    "Happy with my insurance company's service.",
    "Frustrated with my insurance claims delay!",
    "Best insurance options available now.",
    "Insurance policies can be confusing.",
    "Got a great insurance deal today!",
    "Looking for insurance recommendations.",
    "Need advice on the best home insurance.",
    "Which insurance company has the best customer service?",
    "Comparing auto insurance quotes—any tips?",
    "Best dental insurance plans right now?",
    "Looking for affordable travel insurance options.",
    "Anyone know a good health insurance?",
    "Best insurance options available now.",
    "Looking for insurance recommendations.",
    "Need advice on the best home insurance.",
    "Which insurance company has the best customer service?",
    "Comparing auto insurance quotes—any tips?",
    "Best dental insurance plans right now?",
    "Looking for affordable travel insurance options.",
    "Anyone know a good health insurance?",
    "Best insurance options available now.",
    "Car insurance premiums are high this year!",
    "Insurance premiums keep increasing every year!",
    "Why is health insurance so expensive?",
    "Dealing with insurance paperwork is a nightmare!",
    "My insurance agent never responds on time.",
    "Switching insurers because of poor service.",
    "Got a great insurance deal today!",
    "Just renewed my policy at a lower rate!",
    "My insurance company gave me a discount for safe driving.",
    "Highly recommend my insurer—great coverage and prices!",
    "Found a bundle deal for home and auto insurance!",
    "Customer service at my insurance company is top-notch!",
    "Thinking about life insurance, is it worth it?",
    "Is term life insurance better than whole life?",
    "What does renters insurance actually cover?",
    "How much car insurance coverage do I really need?",
    "Are extended warranties worth it, or just insurance?",
    "Does insurance cover pre-existing conditions?",
    "Insurance policies can be confusing.",
]

# Helper function for text selection
def select_text():
    if random.random() < 0.75:  # 75% insurance-related
        return random.choice(insurance_phrases)
    else:  # 25% random
        return fake.sentence(nb_words=random.randint(5, 150))

# Twitter data generation
def generate_twitter_data(n=2000):
    tweets = []
    for _ in range(n):
        tweets.append({
            "id": fake.uuid4(),
            "created_at": random_date(),
            "text": select_text(),
            "user": {
                "id": fake.uuid4(),
                "name": fake.name(),
                "username": fake.user_name()
            },
            "retweet_count": random.randint(0, 100),
            "favorite_count": random.randint(0, 200),
            "lang": "en"
        })
    with open(os.path.join(DATA_DIR, "twitter_data.json"), "w") as f:
        json.dump(tweets, f, indent=2)

# Facebook data generation
def generate_facebook_data(n=2000):
    posts = []
    for _ in range(n):
        posts.append({
            "id": "fb_" + fake.uuid4(),
            "created_time": random_date(),
            "message": select_text(),
            "story": fake.sentence(nb_words=random.randint(5, 150)),
            "from": {
                "name": fake.name(),
                "id": "user_" + fake.uuid4()
            },
            "reactions": {
                "like": random.randint(0, 100),
                "love": random.randint(0, 50),
                "wow": random.randint(0, 20)
            },
            "comments": {
                "count": random.randint(5, 150)
            }
        })
    with open(os.path.join(DATA_DIR, "facebook_data.json"), "w") as f:
        json.dump(posts, f, indent=2)

# Instagram data generation
def generate_instagram_data(n=2000):
    posts = []
    for _ in range(n):
        posts.append({
            "id": "insta_" + fake.uuid4(),
            "timestamp": random_date(),
            "caption": select_text(),
            "media_type": random.choice(["IMAGE", "VIDEO"]),
            "media_url": fake.image_url(),
            "username": fake.user_name(),
            "comments_count": random.randint(0, 50),
            "like_count": random.randint(0, 300)
        })
    with open(os.path.join(DATA_DIR, "instagram_data.json"), "w") as f:
        json.dump(posts, f, indent=2)

# LinkedIn data generation
def generate_linkedin_data(n=2000):
    posts = []
    for _ in range(n):
        posts.append({
            "id": "li_" + fake.uuid4(),
            "created": {
                "time": int((datetime.now() - timedelta(days=random.randint(0, 30))).timestamp() * 1000)
            },
            "text": {
                "text": select_text()
            },
            "author": {
                "name": fake.name(),
                "id": "linkedin_user_" + fake.uuid4()
            },
            "reactionSummary": {
                "count": random.randint(0, 100)
            },
            "commentSummary": {
                "count": random.randint(0, 30)
            }
        })
    with open(os.path.join(DATA_DIR, "linkedin_data.json"), "w")  as f: 
        json.dump(posts, f, indent=2)

# Execute generation
if __name__ == "__main__":
    generate_twitter_data()
    generate_facebook_data()
    generate_instagram_data()
    generate_linkedin_data()
    print("✅ Insurance-focused mock data files generated!")
