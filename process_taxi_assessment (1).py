"""
Data Analyst Assessment — reproducible processing script
Dataset: NYC Yellow Taxi 200,000-row reproducible sample

This script downloads the exact sample, cleans it, calculates KPIs,
exports processed data and summary tables, and creates dashboard-ready CSVs.

Source:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
Sample:
https://datatweets.com/datasets/nyc-taxi/yellow_tripdata_sample.csv
"""

import os
import pandas as pd
import numpy as np

DATA_URL = "https://datatweets.com/datasets/nyc-taxi/yellow_tripdata_sample.csv"
RAW_FILE = "yellow_tripdata_sample.csv"
OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

# 1) Download / load
if not os.path.exists(RAW_FILE):
    import urllib.request
    urllib.request.urlretrieve(DATA_URL, RAW_FILE)

df = pd.read_csv(RAW_FILE)

# 2) Standardize names
df.columns = [c.strip() for c in df.columns]

# 3) Correct data types
for c in ["tpep_pickup_datetime", "tpep_dropoff_datetime"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")

numeric_cols = [
    "passenger_count", "trip_distance", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "tip_amount", "total_amount"
]
for c in numeric_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# 4) Duplicate check
duplicate_rows = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# 5) Calculated fields
df["trip_duration_min"] = (
    df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

payment_map = {
    0: "Unknown / Flex Fare",
    1: "Credit card",
    2: "Cash",
    3: "No charge",
    4: "Dispute",
}
df["payment_category"] = df["payment_type"].map(payment_map).fillna("Other / Unknown")
df["high_fare_flag"] = np.where(df["total_amount"] > 50, "High fare", "Other")

# 6) Quality flags — do not silently delete; flag first
df["invalid_distance_flag"] = (df["trip_distance"] < 0)
df["invalid_duration_flag"] = (df["trip_duration_min"] < 0)
df["extreme_fare_flag"] = (df["total_amount"].abs() > 500)

# 7) Analysis-ready filter
analysis = df[
    (~df["invalid_distance_flag"]) &
    (~df["invalid_duration_flag"])
].copy()

# 8) KPIs
kpis = pd.DataFrame({
    "metric": [
        "rows_raw", "duplicate_rows", "rows_analysis",
        "total_revenue", "avg_trip_value", "avg_trip_distance_mi",
        "high_fare_trips", "high_fare_share", "missing_passenger_count"
    ],
    "value": [
        len(df),
        duplicate_rows,
        len(analysis),
        analysis["total_amount"].sum(),
        analysis["total_amount"].mean(),
        analysis["trip_distance"].mean(),
        (analysis["total_amount"] > 50).sum(),
        (analysis["total_amount"] > 50).mean(),
        analysis["passenger_count"].isna().sum()
    ]
})
kpis.to_csv(os.path.join(OUT_DIR, "kpis.csv"), index=False)

# 9) Payment summary
payment_summary = (
    analysis.groupby("payment_category", dropna=False)
    .agg(trips=("payment_category", "size"),
         revenue=("total_amount", "sum"),
         avg_trip_value=("total_amount", "mean"))
    .reset_index()
)
payment_summary["share"] = payment_summary["trips"] / len(analysis)
payment_summary.to_csv(os.path.join(OUT_DIR, "payment_summary.csv"), index=False)

# 10) Distance-band summary
bins = [-np.inf, 1, 2, 3, 5, 10, np.inf]
labels = ["<=1", "1-2", "2-3", "3-5", "5-10", "10+"]
analysis["distance_band"] = pd.cut(
    analysis["trip_distance"], bins=bins, labels=labels, right=False
)
distance_summary = (
    analysis.groupby("distance_band", observed=False)
    .agg(trips=("trip_distance","size"),
         avg_fare=("total_amount","mean"),
         revenue=("total_amount","sum"))
    .reset_index()
)
distance_summary.to_csv(os.path.join(OUT_DIR, "distance_summary.csv"), index=False)

# 11) Hourly summary
analysis["pickup_hour"] = analysis["tpep_pickup_datetime"].dt.hour
hourly = (
    analysis.groupby("pickup_hour")
    .agg(trips=("pickup_hour","size"),
         revenue=("total_amount","sum"),
         avg_trip_value=("total_amount","mean"))
    .reset_index()
)
hourly.to_csv(os.path.join(OUT_DIR, "hourly_summary.csv"), index=False)

# 12) Final processed data
analysis.to_csv(os.path.join(OUT_DIR, "processed_data.csv"), index=False)

print("Done.")
print(kpis.to_string(index=False))
