from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# Import your actual scripts
import Ingestion_Scripts.ingest_twitter as twitter
import Ingestion_Scripts.ingest_facebook as facebook
import Ingestion_Scripts.ingest_instagram as instagram
import Ingestion_Scripts.ingest_linkedin as linkedin
import run_sentiment_analysis
import combine_sentiment_parquet

default_args = {
    'owner': 'data_team',
    'start_date': datetime(2025, 4, 4),
    'retries': 1,
}

with DAG(
    dag_id='daily_sentiment_analysis_pipeline',
    default_args=default_args,
    schedule_interval='@daily',  # Can be cron-like: '0 6 * * *'
    catchup=False,
    tags=["sentiment", "social", "POC"]
) as dag:

    t1 = PythonOperator(task_id='ingest_twitter', python_callable=twitter.ingest_twitter)
    t2 = PythonOperator(task_id='ingest_facebook', python_callable=facebook.ingest_facebook)
    t3 = PythonOperator(task_id='ingest_instagram', python_callable=instagram.ingest_instagram)
    t4 = PythonOperator(task_id='ingest_linkedin', python_callable=linkedin.ingest_linkedin)

    t5 = PythonOperator(task_id='run_sentiment_analysis', python_callable=run_sentiment_analysis.run_sentiment_pipeline)
    t6 = PythonOperator(task_id='combine_outputs', python_callable=combine_sentiment_parquet.combine_sentiment_outputs)

    # DAG flow
    [t1, t2, t3, t4] >> t5 >> t6
