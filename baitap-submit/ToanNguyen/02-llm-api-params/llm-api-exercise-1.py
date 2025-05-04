#install openai first
#pin install openai

import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key="API_KEY_HERE"
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