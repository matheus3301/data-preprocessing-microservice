#!/usr/bin/env python3
"""
Script to generate a sample Parquet file for testing the Data Preprocessing Microservice.
This script creates a sample DataFrame and saves it as a Parquet file.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Create output directory if it doesn't exist
os.makedirs("examples/data", exist_ok=True)

# Generate sample data
print("Generating sample data...")

# Number of rows
n_rows = 1000

# Create a date range
start_date = datetime.now() - timedelta(days=n_rows)
dates = [start_date + timedelta(days=i) for i in range(n_rows)]

# Generate random data
np.random.seed(42)  # For reproducibility
data = {
    "date": dates,
    "value": np.random.normal(100, 15, n_rows),
    "category": np.random.choice(["A", "B", "C", "D"], n_rows),
    "count": np.random.randint(1, 100, n_rows),
    "valid": np.random.choice([True, False], n_rows, p=[0.9, 0.1])
}

# Create DataFrame
df = pd.DataFrame(data)

# Add some calculated columns
df["value_squared"] = df["value"] ** 2
df["log_count"] = np.log1p(df["count"])

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Convert category to categorical
df["category"] = df["category"].astype("category")

# Output file path
output_file = "examples/data/sample.parquet"

# Save as Parquet
df.to_parquet(output_file, index=False)

print(f"Sample data saved to {output_file}")
print(f"DataFrame shape: {df.shape}")
print("\nDataFrame info:")
print(df.info())
print("\nDataFrame head:")
print(df.head())

# Print instructions for MinIO upload
print("\nTo upload this file to MinIO, you can use the MinIO Client (mc):")
print("1. Install mc: https://min.io/docs/minio/linux/reference/minio-mc.html")
print("2. Configure mc:")
print("   mc alias set myminio http://localhost:9000 minioadmin minioadmin")
print("3. Create a bucket:")
print("   mc mb myminio/my-bucket")
print("4. Upload the file:")
print(f"   mc cp {output_file} myminio/my-bucket/data/")
print("\nOr use the MinIO web console at http://localhost:9001") 