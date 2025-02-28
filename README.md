# Data Preprocessing Microservice

A microservice for processing datasets with custom Python code. This service allows users to apply custom transformations to datasets stored in MinIO using Python code, with the results saved back to MinIO in Parquet format.

## Features

- Process datasets using custom Python code
- Support for various input formats (Parquet, CSV, Excel, JSON)
- Results saved in efficient Parquet format
- Secure code execution in a sandbox environment
- Resource limits for code execution (memory, CPU, time)

## Architecture

The microservice is designed to be stateless and follows a clean architecture pattern:

- **API Layer**: FastAPI endpoints for receiving requests
- **Service Layer**: Core business logic for code validation, execution, and MinIO interaction
- **Schema Layer**: Pydantic models for request/response validation

## Requirements

- Python 3.11+
- MinIO server
- uv (for dependency management)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/data-preprocessing-microservice.git
   cd data-preprocessing-microservice
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. For development, install development dependencies:
   ```bash
   uv pip install -r requirements-dev.txt
   ```

## Configuration

The service can be configured using environment variables:

- `DEBUG`: Enable debug mode (default: False)
- `MINIO_ENDPOINT`: MinIO server endpoint (default: localhost:9000)
- `MINIO_ACCESS_KEY`: MinIO access key (default: minioadmin)
- `MINIO_SECRET_KEY`: MinIO secret key (default: minioadmin)
- `MINIO_SECURE`: Use HTTPS for MinIO connection (default: False)

You can also create a `.env` file in the root directory with these variables.

## Running the Service

Start the service with:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

### Process Dataset

```
POST /api/v1/process
```

Request body:
```json
{
  "dataset_path": "bucket-name/path/to/dataset.parquet",
  "code": "import pandas as pd\n\ndef process(df):\n    df['new_column'] = df['existing_column'] * 2\n    return df",
  "timeout": 120,
  "max_memory": 2048
}
```

Response:
```json
{
  "status": "success",
  "parquet_path": "bucket-name/processed/1620000000_abcd1234.parquet",
  "rows": 1000,
  "columns": ["existing_column", "new_column"],
  "execution_time": 0.5,
  "metadata": {
    "input_path": "bucket-name/path/to/dataset.parquet",
    "input_format": "parquet",
    "timestamp": 1620000000
  }
}
```

## Supported Input Formats

The service can process datasets in the following formats:
- **Parquet** (optimized for performance)
- CSV
- Excel (xls, xlsx)
- JSON

All results are saved in Parquet format for efficient storage and retrieval.

## Code Validation

The service validates user code to ensure it's safe to execute:

- Only allowed imports (pandas, numpy, pycatch22)
- No dangerous function calls (eval, exec, etc.)
- Must define a `process` function that takes a DataFrame and returns a DataFrame

## Sandbox Execution

Code is executed in a sandbox environment with:

- Limited memory usage
- Execution timeout
- No access to the filesystem, network, or system resources

## Development

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- Ruff for linting
- mypy for type checking

Run the formatters and linters:
```bash
black .
isort .
ruff .
mypy .
```

### Testing

Run tests with pytest:
```bash
pytest
```

