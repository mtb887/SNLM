Mock Data Generation
📁 Data Storage
All mock data files used in this Proof of Concept (POC) are stored within the project's Data folder:

pgsql
Copy
Edit
📂 Project Root
 ├── 📂 Data
 │    ├── twitter_data.json
 │    ├── facebook_data.json
 │    ├── instagram_data.json
 │    └── linkedin_data.json
🚧 Purpose of Mock Data
For the purposes of the Proof of Concept (POC), direct API calls to social media platforms are avoided due to complexity, API access limitations, and rate limiting concerns.

Instead, we generate mock data simulating the structure and contents of actual social media API responses. This allows rapid, reliable, and repeatable testing of the data ingestion, processing, and sentiment analysis pipeline.

In a full production deployment, actual social media APIs will replace these mock files.

🛠️ How Mock Data is Generated
Mock data is generated using a Python script named generate_mock_data.py. This script leverages Python's faker library to create realistic social media post data.

✅ Steps to Generate Mock Data:
Install Dependencies

bash
Copy
Edit
pip install faker
Execute the Python Script

Run this command from your project's root directory:

bash
Copy
Edit
python generate_mock_data.py
Output

After execution, the following files (each with 500 records) are created inside your Data directory:

twitter_mock.json

facebook_mock.json

instagram_mock.json

linkedin_mock.json

📜 Mock Data Format per Platform
Each mock data file mimics real API structures, ensuring compatibility with downstream ingestion processes:

🐦 Twitter (twitter_mock.json)
Tweet ID, creation timestamp, tweet text (75% insurance-related), user details, retweets, favorites, language.

📘 Facebook (facebook_mock.json)
Post ID, created timestamp, message (75% insurance-related), story, user details, reaction counts, comment counts.

📸 Instagram (instagram_mock.json)
Post ID, timestamp, caption (75% insurance-related), media type (image/video), media URL, username, comments, likes.

🔗 LinkedIn (linkedin_mock.json)
Post ID, created timestamp, text content (75% insurance-related), author details, reaction summary, comment summary.

🔎 Script Explanation (generate_mock_data.py):
The Python script performs these tasks:

Initialization:
Initializes a Faker object for realistic text, dates, and names.

Insurance-Related Content:
Pre-defines a list of phrases specifically related to insurance topics. Randomized selection ensures about 75% of generated posts are insurance-focused.

Randomized Timestamps:
Uses recent random timestamps (within the last 30 days) to simulate realistic posting dates.

Platform-Specific Structures:
Structures each JSON object to closely replicate the expected real-world API responses for each social media platform.

Writes JSON Files:
Writes 500 generated records per platform directly to their respective JSON files in the Data folder.

🚀 From POC to Production:
⚠️ POC (Current Implementation):
No external API usage.

Uses mock data to reliably test pipeline functionality, processing logic, and sentiment analysis results.

✅ Production Implementation (Future State):
Will replace mock JSON files with real-time API calls to:

Twitter API via Tweepy (or X v2 API)

Facebook Graph API

Instagram Basic Display API / Graph API

LinkedIn API

Adjustments in data ingestion scripts will handle authentication, pagination, rate limits, and error handling from the respective APIs.