import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path from which to run the python file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list",
                    "description": "List of string arguments to pass to the python file",
                },
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        result = f"Result for {file_path} file"

        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return result + f'\n\tError: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return result + f'\n\tError: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return result + f'\n\tError: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args: command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, text=True, timeout=30, capture_output=True)
        
        if completed_process.returncode != 0:
            return result + f'\n\tProcess exited with code {completed_process.returncode}'
        if len(completed_process.stdout + completed_process.stderr) == 0:
            return result + f'\n\tNo output produced'

        return result + f'\n\tSTDOUT:\n{completed_process.stdout}' + f'\tSTDERR:\n{completed_process.stderr}'
        
    except Exception as e:
        return f'Error: exectuing python file {e}'