
## 🛠️ Installation & Setup Instructions

### Step 1: Set Up Python Environment

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
.env\Scripts_ctivate       # Windows
```

### Step 2: Install Project Dependencies

Install all necessary libraries:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Use

### Step 1: Generate Social Media Mock Data

This step creates sample JSON files with 500 social media posts per platform:

```bash
python generate_mock_data.py
```

Output files will be saved in the `Data/` folder:
- `twitter_mock.json`
- `facebook_mock.json`
- `instagram_mock.json`
- `linkedin_mock.json`

---

### Step 2: Run the Ingestion Pipelines

This filters insurance-related posts, removes sensitive user details, and writes sanitized versions to `Ingested/`.

```bash
python run_ingestion.py
```

Outputs:
- `Ingested/twitter_insurance.json`
- `Ingested/facebook_insurance.json`
- `Ingested/instagram_insurance.json`
- `Ingested/linkedin_insurance.json`
- `Ingested/raw/` → Raw, PII-containing original files

---

## 🔐 Data Privacy & PII Protection

This project includes built-in mechanisms for GDPR and POPIA compliance:

- No names or usernames are stored or logged.
- Sensitive fields are removed or hashed (SHA-256).
- Raw data is separated from cleaned output in `Ingested/raw/`.
- Sanitization logic resides in `Ingestion/pii_sanitizer.py`.

---

## 🧾 Required Python Packages

Below is the complete list of dependencies found in `requirements.txt`:

```
pandas>=1.5.0
faker==19.6.2
nltk==3.8.1
textblob==0.17.1
vaderSentiment==3.3.2
pyspark==3.4.1
kafka-python==2.0.2
streamlit==1.29.0
apache-airflow==2.8.1
pytest>=7.0
```

Install all of them with:

```bash
pip install -r requirements.txt
```

---

## 🏁 Conclusion

This project serves as a fully functional proof of concept for analyzing public sentiment on insurance products using social media data. It is built with compliance, modularity, and clarity in mind. Follow the steps in this manual to run the full pipeline end-to-end.