import os
import traceback
from dotenv import load_dotenv
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from open_ai import OpenAi
from youtube import Youtube
load_dotenv()

test=[{'role': 'system', 'content': "In each message I will list trending keywords from google. Your job is to make out ifthey are related to a product, service, or videogame that is being produced by a publiclytraded company. If you find a match, respond with the keyword list from the message, as well as the company and its stock ticker. Also provide your reasoning in single sentence.If the keywords do not match to any company, reply only with 'false'."}, {'role': 'user', 'content': "['Smosh', 'Ian Hecox', 'Anthony Padilla', 'Rhett and Link', 'YouTube']"}, {'role': 'user', 'content': "['Tablet computer', 'Google Pixel', 'Android']"}]

# get youtube data
try:
    youtube_text = OpenAi(Youtube()())()
    if not youtube_text:
        youtube_text='No relevant videos found'
except Exception as e:
    youtube_text = traceback.format_exc()

# get google data
try:
    # google_text = OpenAi(Google()())()
    google_text = OpenAi(test)()
    if not google_text:
        google_text='No relevant trends found'
except Exception as e:
    google_text = traceback.format_exc()

print(youtube_text + '\n\n' + google_text)
# setup email
# sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
# from_email = Email(os.getenv('FROM_EMAIL'))
# to_email = To(os.getenv('TO_EMAIL'))
# subject = "Trends report"
# content = Content("text/plain", youtube_text)
# mail = Mail(from_email, to_email, subject, content)
# try:
#     response = sg.client.mail.send.post(request_body=mail.get())
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e)

