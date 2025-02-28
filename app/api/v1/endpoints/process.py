import time
import uuid
import os
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.schemas.process import ProcessRequest, ProcessResponse, ErrorResponse
from app.services.code_validator import code_validator
from app.services.code_executor import code_executor
from app.services.minio_client import minio_client

router = APIRouter()


@router.post(
    "/process",
    response_model=ProcessResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Process a dataset with custom code",
    description="Process a dataset from MinIO using custom Python code and save the result as a Parquet file",
)
async def process_dataset(request: ProcessRequest):
    """
    Process a dataset with custom Python code.
    
    The code must define a 'process' function that takes a DataFrame and returns a DataFrame.
    The function will be executed in a sandbox environment with limited resources.
    
    Args:
        request: The process request containing the dataset path and code
        
    Returns:
        A response containing the path to the generated Parquet file and metadata
    """
    # Validate the code
    is_valid, validation_result = code_validator.validate_code(request.code)
    
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=validation_result
        )
    
    try:
        # Load the dataset from MinIO
        try:
            df, file_extension = minio_client.load_dataset(request.dataset_path)
        except ValueError as e:
            raise HTTPException(
                status_code=404,
                detail={"error": str(e)}
            )
        
        # Execute the code
        success, execution_result = code_executor.execute_code(
            code=request.code,
            df=df,
            timeout=request.timeout,
            max_memory=request.max_memory
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail={"error": execution_result["error"]}
            )
        
        # Generate a unique name for the result file
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        
        # Extract bucket name and object name from the input path
        input_bucket, input_object = request.dataset_path.split("/", 1)
        
        # Create a directory structure similar to the input path
        input_dir = os.path.dirname(input_object)
        input_filename = os.path.basename(input_object).split(".")[0]
        
        # Create the output path
        if input_dir:
            result_object_name = f"{input_dir}/processed/{input_filename}_{timestamp}_{unique_id}.parquet"
        else:
            result_object_name = f"processed/{input_filename}_{timestamp}_{unique_id}.parquet"
        
        # Save the result DataFrame to MinIO
        result_path = minio_client.save_dataframe(
            df=execution_result["result_df"],
            bucket_name=input_bucket,
            object_name=result_object_name
        )
        
        # Create the response
        response = ProcessResponse(
            status="success",
            parquet_path=result_path,
            rows=execution_result["rows"],
            columns=execution_result["columns"],
            execution_time=execution_result["execution_time"],
            metadata={
                "input_path": request.dataset_path,
                "input_format": file_extension,
                "timestamp": timestamp,
                "original_filename": input_filename
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": f"An unexpected error occurred: {str(e)}"}
        ) 