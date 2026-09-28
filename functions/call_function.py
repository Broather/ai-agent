import json
from collections.abc import Callable
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args: dict = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    if function_name in function_map:
        function_args["working_directory"] = "./calculator"
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"{function_map[function_name](**function_args)}"
        }
    else:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }