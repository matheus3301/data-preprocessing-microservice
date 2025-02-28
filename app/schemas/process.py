from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


class ProcessRequest(BaseModel):
    dataset_path: str = Field(..., description="Path to the dataset in MinIO")
    code: str = Field(..., description="Python code containing a process function")
    timeout: Optional[int] = Field(None, description="Timeout in seconds")
    max_memory: Optional[int] = Field(None, description="Maximum memory in MB")
    max_cpu: Optional[float] = Field(None, description="Maximum CPU cores")

    @validator("code")
    def validate_code_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v


class ProcessResponse(BaseModel):
    status: str = Field(..., description="Status of the processing")
    parquet_path: str = Field(..., description="Path to the generated Parquet file")
    rows: int = Field(..., description="Number of rows in the result DataFrame")
    columns: List[str] = Field(..., description="Columns in the result DataFrame")
    execution_time: float = Field(..., description="Execution time in seconds")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ErrorResponse(BaseModel):
    status: str = Field("error", description="Error status")
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details") 