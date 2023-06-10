import os
from dotenv import load_dotenv
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from youtube_open_ai import YoutubeOpenAi
load_dotenv()

sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
from_email = Email("joona.rotko@outlook.com")
to_email = To("joona.rotko@outlook.com")
subject = "Trends report"
content = Content("text/plain", YoutubeOpenAi()())
mail = Mail(from_email, to_email, subject, content)
try:
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
