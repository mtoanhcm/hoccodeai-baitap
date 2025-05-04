#install openai first
#pin install openai

import os
import re
import subprocess
from openai import OpenAI

RED = "\033[91m"
RESET = "\033[0m"

client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key="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"
    )
        
def get_user_request():
    user_request = input("Enter your program exercise: ")
    messages = [
        {
            "role": "system",
            "content": "You are a senior software engineer assistant that can help me resolve program exercise"
        },
        {
            "role": "user",
            "content": f"""
            Write a Python program to:
            {user_request}
            Only return the Python code. Do not include explanations or descriptions.
            Wrap the entire code inside one single code block like this:
            ```python
            #all code here
            ```
            """
        }
    ]
    return messages

def resolve_program_exercise(prompt):
    response = client.chat.completions.create(
        model="o4-mini-2025-04-16",
        messages=prompt,
        temperature=1,
        )
    content = response.choices[0].message.content
    print(content)
    finalCode = re.search(r"```(?:python)?\n(.*?)```", content, re.DOTALL)
    if finalCode:
        return finalCode.group(1).strip()
    else:
        return None

def save_code_to_file(code):
    output_file = input("Enter output file name: ")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path  = os.path.join(script_dir, f"{output_file}.py")
    with open(output_path, "w") as file:
        file.write(code)

    return output_path

def main():
    try:
        while True:
            user_request = get_user_request()
            code = resolve_program_exercise(user_request)
            if code:
                file_path = save_code_to_file(code)
                #subprocess.run(["python", "-c", code])
                subprocess.run(["python", file_path])
            else:
                print(f"{RED}No code found{RESET}")
            break
    except (KeyboardInterrupt, EOFError):
        print(f"{RED}Input error, END{RESET}")

main()