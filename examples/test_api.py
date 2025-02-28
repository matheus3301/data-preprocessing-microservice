#!/usr/bin/env python3
"""
Example script to test the Data Preprocessing Microservice API.
This script demonstrates how to send a request to process a dataset.
"""

import requests
import json
import time

# API endpoint
API_URL = "http://localhost:8000/api/v1/process"

# Example code that processes a DataFrame
CODE = """
import pandas as pd
import numpy as np

def process(df):
    if 'value' in df.columns:
        df['rolling_mean'] = df['value'].rolling(window=3).mean()
    else:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            first_numeric = numeric_cols[0]
            df['rolling_mean'] = df[first_numeric].rolling(window=3).mean()
        else:
            df['rolling_mean'] = range(len(df))
    
    df = df.dropna()
    
    df['timestamp'] = pd.Timestamp.now()
    
    return df
"""

# Request data
payload = {
    "dataset_path": "matheus/sample.parquet",  # Replace with your actual dataset path
    "code": CODE,
    "timeout": 120,
    "max_memory": 2048
}

print(f"Sending request to {API_URL}...")
start_time = time.time()

print("\nEquivalent curl command:")
print(f"""curl -X POST {API_URL} \\
    -H "Content-Type: application/json" \\
    -d '{json.dumps(payload)}'""")

try:
    response = requests.post(API_URL, json=payload)
    
    print(f"\nStatus code: {response.status_code}")
    print(f"Response time: {time.time() - start_time:.2f} seconds")
    
    if response.status_code == 200:
        result = response.json()
        print("\nSuccess!")
        print(f"Parquet file: {result['parquet_path']}")
        print(f"Rows: {result['rows']}")
        print(f"Columns: {', '.join(result['columns'])}")
        print(f"Execution time: {result['execution_time']:.2f} seconds")
        print("\nMetadata:")
        for key, value in result['metadata'].items():
            print(f"  {key}: {value}")
    else:
        print("\nError:")
        print(json.dumps(response.json(), indent=2))
        
except Exception as e:
    print(f"Error: {str(e)}")