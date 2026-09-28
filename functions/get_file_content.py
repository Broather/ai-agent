import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads a file in a specified directory relative to the working directory. If the file is too large, a truncation message is appened at the end",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path from which to read the file, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    result = f"Result for {file_path} file"
        
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    if not os.path.isfile(target_file_path):
        return result + f'\n\tError: File not found or is not a regular file: "{file_path}"'
    
    valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    if not valid_target_file_path:
        return result + f'\n\tError: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except:
        return f"Error: Failed to read file"
        
    return content