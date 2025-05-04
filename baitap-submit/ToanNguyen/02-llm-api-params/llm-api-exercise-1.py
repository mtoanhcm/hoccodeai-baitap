#install openai first
#pin install openai

import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key="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"
    )

def main():
    try:
        while True:
            ask_ai(input())
    except (KeyboardInterrupt, EOFError):
        print("Input error, END")
        
def ask_ai(question):
    response = client.chat.completions.create(
        model="o4-mini-2025-04-16",
        messages=[
            {
                "role": "user", 
                "content": question
            }
        ],
        stream = True)

    for chunk in response:
      print(chunk.choices[0].delta.content or "", end="")

    print()

main()