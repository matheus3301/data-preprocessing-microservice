import time
import traceback
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
import importlib
import sys
import resource
import signal
from contextlib import contextmanager

from app.core.config import settings


class TimeoutException(Exception):
    """Exception raised when code execution times out."""
    pass


@contextmanager
def time_limit(seconds: int):
    """
    Context manager to limit execution time.
    
    Args:
        seconds: Maximum execution time in seconds
    """
    def signal_handler(signum, frame):
        raise TimeoutException("Code execution timed out")
    
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def set_resource_limits(max_memory_mb: int):
    """
    Set resource limits for the current process.
    
    Args:
        max_memory_mb: Maximum memory in MB
    """
    # Convert MB to bytes
    max_memory_bytes = max_memory_mb * 1024 * 1024
    
    # Set memory limit
    resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))


class CodeExecutor:
    def __init__(self):
        pass
    
    def execute_code(
        self, 
        code: str, 
        df: pd.DataFrame, 
        timeout: Optional[int] = None,
        max_memory: Optional[int] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Execute the user's code in a sandbox environment.
        
        Args:
            code: Python code to execute
            df: Input DataFrame
            timeout: Maximum execution time in seconds
            max_memory: Maximum memory in MB
            
        Returns:
            Tuple containing a boolean indicating if the execution was successful and a dictionary with execution details
        """
        # Set default values if not provided
        timeout = timeout or settings.DEFAULT_TIMEOUT
        max_memory = max_memory or settings.DEFAULT_MAX_MEMORY
        
        # Create a namespace for execution
        namespace = {
            "pd": pd,
            "numpy": np,
            "np": np,
        }
        
        # Try to import pycatch22 if available
        try:
            import pycatch22
            namespace["pycatch22"] = pycatch22
        except ImportError:
            pass
        
        # Add the input DataFrame to the namespace
        # Make a copy to prevent modifications to the original
        namespace["input_df"] = df.copy()
        
        try:
            # Set resource limits
            set_resource_limits(max_memory)
            
            # Execute the code with a time limit
            with time_limit(timeout):
                start_time = time.time()
                
                # Execute the user's code
                exec(code, namespace)
                
                # Check if the process function exists
                if "process" not in namespace or not callable(namespace["process"]):
                    return False, {
                        "success": False,
                        "error": "No 'process' function found in the code",
                        "execution_time": time.time() - start_time
                    }
                
                # Call the process function with the input DataFrame
                result_df = namespace["process"](namespace["input_df"])
                
                # Check if the result is a DataFrame
                if not isinstance(result_df, pd.DataFrame):
                    return False, {
                        "success": False,
                        "error": "The 'process' function must return a DataFrame",
                        "execution_time": time.time() - start_time
                    }
                
                # Optimize the DataFrame for Parquet storage
                # Convert object columns to categorical if they have few unique values
                for col in result_df.select_dtypes(include=['object']).columns:
                    if result_df[col].nunique() < len(result_df) * 0.5:  # If less than 50% unique values
                        result_df[col] = result_df[col].astype('category')
                
                execution_time = time.time() - start_time
                
                return True, {
                    "success": True,
                    "result_df": result_df,
                    "execution_time": execution_time,
                    "rows": len(result_df),
                    "columns": list(result_df.columns)
                }
        
        except TimeoutException:
            return False, {
                "success": False,
                "error": f"Code execution timed out after {timeout} seconds"
            }
        except MemoryError:
            return False, {
                "success": False,
                "error": f"Code execution exceeded memory limit of {max_memory} MB"
            }
        except Exception as e:
            return False, {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }


# Singleton instance
code_executor = CodeExecutor() 