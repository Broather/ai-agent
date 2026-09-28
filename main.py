import argparse
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def generate_content(client, messages, tools):
        return client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=tools,
            temperature=0
        )

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    prompt: str = args.user_prompt
    is_verbose: bool = args.verbose

    available_functions = [
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        schema_get_files_info
    ]
    
    messages = [
            {"role":"system", "content": system_prompt},
            {"role":"user", "content": prompt},
        ]
    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    response = generate_content(client, messages, available_functions)

    if is_verbose:
        print(f"User prompt: {prompt}")
        print(f"Model used: {response.model}")
        if response.usage:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("Response doen not have a usage property")

    print("Response:")
    message = response.choices[0].message
    
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, is_verbose)
            if len(result_message["content"]) == 0:
                raise RuntimeError("Result content is empty")
            if is_verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)

if __name__ == "__main__":
    main()
