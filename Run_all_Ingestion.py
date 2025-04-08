import subprocess

# List of scripts to run
scripts = [
    "Ingestion_Scripts/ingest_twitter.py",
    "Ingestion_Scripts/ingest_facebook.py",
    "Ingestion_Scripts/ingest_instagram.py",
    "Ingestion_Scripts/ingest_linkedin.py"
]

print(" Starting full ingestion process...\n")

for script in scripts:
    print(f"▶ Running {script}")
    result = subprocess.run(["python", script], capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error running {script}:\n{result.stderr}")

print(" All ingestion pipelines complete.")
print(" Starting data processing...\n" )