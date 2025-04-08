import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Social Media Insurance Sentiment Dashboard", layout="wide")

# ----------------------------
# Load most recent parquet file
# ----------------------------
from datetime import datetime, timedelta

def get_latest_file():
    base_path = "Processed_Data"
    
    # Try today first, then yesterday
    for offset in [0, 1]:
        day = datetime.today() - timedelta(days=offset)
        year = str(day.year)
        month = str(day.month).zfill(2)
        day_str = str(day.day).zfill(2)
        file_path = os.path.join(base_path, year, month, day_str, "combined_sentiment.parquet")

        if os.path.exists(file_path):
            st.success(f"✅ Loaded sentiment data for {year}-{month}-{day_str}")
            return pd.read_parquet(file_path)

    st.warning("No data found for today or yesterday.")
    return pd.DataFrame()


df = get_latest_file()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.title("📊 Filters")

if not df.empty:
    platforms = st.sidebar.multiselect("Platform", df["platform"].unique(), default=df["platform"].unique())
    sentiments = st.sidebar.multiselect("Sentiment", df["sentiment"].unique(), default=df["sentiment"].unique())
    min_score, max_score = st.sidebar.slider("Sentiment Score Range", -1.0, 1.0, (-1.0, 1.0), 0.01)

    filtered = df[
        df["platform"].isin(platforms) &
        df["sentiment"].isin(sentiments) &
        df["score"].between(min_score, max_score)
    ]

    # ----------------------------
    # Charts
    # ----------------------------
    st.title("📈 Social Sentiment Overview")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment Count")
        st.bar_chart(filtered["sentiment"].value_counts())

    with col2:
        st.subheader("Platform Distribution")
        st.bar_chart(filtered["platform"].value_counts())

    st.subheader("📋 Sample Posts")
    st.dataframe(filtered[["platform", "sentiment", "score", "text", "timestamp"]].sort_values("score", ascending=False), height=400)

else:
    st.warning("No sentiment data available for today.")
