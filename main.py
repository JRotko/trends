import os
import traceback
from dotenv import load_dotenv
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from open_ai import OpenAi
from youtube import Youtube
load_dotenv()

# get youtube data
try:
    youtube_text = OpenAi(Youtube()())()
    if not youtube_text:
        youtube_text='No relevant videos found'
except Exception as e:
    youtube_text = traceback.format_exc()

print(youtube_text)
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

