#Install first
#pip install openai langcodes

#Eimport openai
import os
from openai import OpenAIError
from openai import OpenAI
import langcodes

RED = "\033[91m"
RESET = "\033[0m"

client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key=""
    )

def process_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    return "\n".join(paragraphs)

def check_language_code(language_name):
    try:
        lang = langcodes.find(language_name)
        return lang.display_name()
    except LookupError:
        print(f'{RED}Error: "{language_name}" is not a recognized language name.{RESET}')
        return None
        
def finalize_content_to_prompt(paragraph, language_name, translate_style):
    messages = [
        {
            "role": "system",
            "content": "You are a experience translator. You can translate texts in different styles like serious, funny or emotional."
        }
    ]
    prompt = f"""
        You are my translator assistant. Please follow these guidelines:
        1. Translate the text into {language_name}
        2. Maintain the {translate_style} style in the translation
        3. Keep the original meaning and context
        4. Ensure natural flow in the target language
        5. Pay attention to cultural nuances
        
        Text to translate:
        {paragraph}
        
        Please provide the translation only, without explanations.
        """
    messages.append({"role":"user","content":prompt})
    return messages

def send_request(message_request):
    try:
        request = client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages= message_request
        )

        #print(request.choices[0].message.content)
        return request.choices[0].message.content
    except OpenAIError as error:
        print(f"{RED}Error: {error}{RESET}")

def s(paragraph):
    output_file = input("Enter output file name: ")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path  = os.path.join(script_dir, output_file)
    with open(output_path , "w", encoding="utf-8") as file:
        file.write(paragraph + "\n")

def main():
    while True:
        translate_language = input("Enter the language to translate: ")
        language_name = check_language_code(translate_language)
        if language_name:
            break
        print(f"{RED}Please enter a valid language name by English.{RESET}")

    translate_style = input("Enter the style of translation: ")

    while True:
        file_path = input("Enter the path to your text file: ")
        if os.path.isfile(file_path):
            break
        print(f"{RED}Error: File not found. Please check the file path and try again.{RESET}")

    try:
        text_content = process_text_file(file_path)
        if text_content:
            message_result = ""
            for paragraph in text_content.split("\n"):
                if paragraph.strip():
                    print(f"Translating paragraph: {paragraph}")
                    try:
                        translated_text = send_request(finalize_content_to_prompt(paragraph, language_name, translate_style))
                        message_result += translated_text + "\n\n"
                    except Exception as e:
                        print(f"{RED}Error translating paragraph: {e}{RESET}")
                        continue

            extract_translated_paragraph_to_text_file(message_result)
    except Exception as e:
        print(f"{RED}Error: An unexpected error occurred: {e}{RESET}")

main()