import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

def generate_content(client, messages):
        return client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
        )

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    prompt: str = args.user_prompt
    is_verbose: bool = args.verbose

    messages = [
            {"role":"user", "content": prompt},
        ]
    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    response = generate_content(client, messages)

    if is_verbose:
        print(f"User prompt: {prompt}")
        print(f"Model used: {response.model}")
        if response.usage:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("Response doen not have a usage property")

    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
