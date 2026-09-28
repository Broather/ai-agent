import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a file in a specified directory relative to the working directory. If file doesn't exist, it will be created before writing",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to which to write the file, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Text that will replace any existing text in the file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    result = f"Result for {file_path} file"

    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    if os.path.isdir(target_file_path):
        return result + f'\n\tError: Cannot write to "{file_path}" as it is a directory'

    valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
    if not valid_target_file_path:
        return result + f'\n\tError: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # make sure file path exists
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

    try:
        with open(target_file_path, "w") as f:
            f.write(content)
    except:
        return result + f"\n\tError: Failed to write to file"

    return result + f'\n\tSuccessfully wrote to "{file_path}" ({len(content)} characters written)'
