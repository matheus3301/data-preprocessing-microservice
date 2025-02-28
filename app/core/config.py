from typing import List
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Data Preprocessing Microservice"
    PROJECT_DESCRIPTION: str = "Microservice for processing datasets with custom Python code"
    VERSION: str = "0.1.0"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    CORS_ORIGINS: List[str] = ["*"]
    
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "False").lower() == "true"
    
    DEFAULT_TIMEOUT: int = 120
    DEFAULT_MAX_MEMORY: int = 2048
    DEFAULT_MAX_CPU: float = 1.0
    
    ALLOWED_IMPORTS: List[str] = ["pandas", "numpy", "pycatch22"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 