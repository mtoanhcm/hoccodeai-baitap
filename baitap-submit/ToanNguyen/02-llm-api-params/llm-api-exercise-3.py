#Install first
#pip install requests beautifulsoup4 openai

import requests
from bs4 import BeautifulSoup
import openai

max_website_paragraph_character = 10000
client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key=""
    )

def get_website_info(url, target_class):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not get the website. {e}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    target_content = soup.find(class_=target_class)
    if target_content:
        paragraphs = [p.text.strip() for p in target_content.find_all('p') if p.text.strip()]
        return "\n".join(paragraphs)
    return None

def summarize_info(paragraph):
    if len(paragraph) > max_website_paragraph_character:
        paragraph = paragraph[0:max_website_paragraph_character]

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    prompt = f"""
        You are my professional assistant. Please summarize the following paragraph content:
        {paragraph}
        Provide a concise summary covering the key point and make it like a report in Vietnamese.
        """
    messages.append({"role":"user","content":prompt})
    return messages

def send_request(message_request):
    try:
        request = client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages= message_request
        )

        print(request.choices[0].message.content)
    except OpenAIError as error:
        print(f"Error: {error}")

def main():
    url_input = input()
    #I had tried to hardcode with div main-detail as suggested in the lesson. But the crawl data is too wide. So I reviewed the code of the target web and got class "detail-cmain clearfix" instead
    website_pargraph = get_website_info(url_input, "detail-cmain clearfix")
    #print(website_pargraph)
    if website_pargraph is not None:
        send_request(summarize_info(website_pargraph))

main()