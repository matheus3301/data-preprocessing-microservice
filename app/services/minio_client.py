import io
from typing import Tuple, Optional
import pandas as pd
from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )

    def load_dataset(self, path: str) -> Tuple[pd.DataFrame, str]:
        """
        Load a dataset from MinIO and convert it to a pandas DataFrame.
        
        Args:
            path: Path to the dataset in MinIO (bucket/object)
            
        Returns:
            Tuple containing the DataFrame and the file extension
        """
        try:
            # Split the path into bucket and object name
            parts = path.split("/", 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid path format: {path}. Expected format: bucket/object")
            
            bucket_name, object_name = parts
            
            # Check if bucket exists
            if not self.client.bucket_exists(bucket_name):
                raise ValueError(f"Bucket does not exist: {bucket_name}")
            
            # Determine file type from extension
            file_extension = object_name.split(".")[-1].lower()
            
            # Get the object
            response = self.client.get_object(bucket_name, object_name)
            
            # Read the data into a DataFrame based on file type
            if file_extension == "csv":
                df = pd.read_csv(response)
            elif file_extension == "parquet":
                # For Parquet files, we need to read the entire content first
                content = response.read()
                df = pd.read_parquet(io.BytesIO(content))
            elif file_extension in ["xls", "xlsx"]:
                df = pd.read_excel(response)
            elif file_extension == "json":
                df = pd.read_json(response)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            return df, file_extension
            
        except S3Error as e:
            raise ValueError(f"Error accessing MinIO: {str(e)}")
        finally:
            if 'response' in locals():
                response.close()
                response.release_conn()

    def save_dataframe(self, df: pd.DataFrame, bucket_name: str, object_name: str) -> str:
        """
        Save a DataFrame as a Parquet file in MinIO.
        
        Args:
            df: DataFrame to save
            bucket_name: Name of the bucket
            object_name: Name of the object (should end with .parquet)
            
        Returns:
            Path to the saved file (bucket/object)
        """
        try:
            # Ensure the object name ends with .parquet
            if not object_name.endswith(".parquet"):
                object_name = f"{object_name}.parquet"
            
            # Check if bucket exists, create if not
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            
            # Convert DataFrame to Parquet and save to MinIO
            parquet_buffer = io.BytesIO()
            df.to_parquet(parquet_buffer)
            parquet_buffer.seek(0)
            
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=parquet_buffer,
                length=parquet_buffer.getbuffer().nbytes,
                content_type="application/octet-stream",
            )
            
            return f"{bucket_name}/{object_name}"
            
        except S3Error as e:
            raise ValueError(f"Error saving to MinIO: {str(e)}")


# Singleton instance
minio_client = MinioClient() 