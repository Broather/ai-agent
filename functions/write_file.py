import os

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
    if not os.path.exists(target_file_path):
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

    try:
        with open(target_file_path, "w") as f:
            f.write(content)
    except:
        return result + f"\n\tError: Failed to write to file"

    return result + f'\n\tSuccessfully wrote to "{file_path}" ({len(content)} characters written)'
