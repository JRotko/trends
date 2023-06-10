from googleapiclient.discovery import build
import openai
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')

messages = [
    {"role": "system", "content": "I will post ten most trending youtube video titles along the channel names. Your objective is to find if the topics have any relation to stock market"},
    {"role": "user", "content": prompt}
]


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=500
)

if response and 'choices' in response:
    # Successful API call
    # result = response.choices[0].text.strip()
    print(response)
else:
    # Error in API call
    print(f"Error: {response['error']['message']}")