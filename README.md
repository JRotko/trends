# Setup

1. run `pip install -r requirements.txt` from the project root
2. set api keys in `.env-example` and rename it to `.env`
3. run `main.py`

Use windows scheduler to automate the script
https://datatofish.com/python-script-windows-scheduler/

## Youtube api

The youtube api enables access to most viewed videos. We parse the videos by the time of upload,
so the videos that remain can be considered trending. By default it checks for videos that were uploaded
within 24hrs. In testing this yielded usually 1-3 videos. The time can be changed in `youtube.py` `_find_recent_videos`

## Google api

The api returns trending topics in groups that have 1-5 keywords that are related to eachother like:
`['Tablet computer', 'Google Pixel', 'Android']`
We use the `pytrends` library. Google does not have official api for trends, so this library has some own methods to scrape the data.

## OpenAI

Instructions are in their corresponding txt files. GPT-3.5 is not suitable enough to follow the instructions perfectly. For example
private companies appear more than often, and it never can respond only with 'false' when a match is not found. Migrate to gpt-4 as
soon as it comes publicly available to API.

## Sendgrid

Its hard to receive sendgrid messages to outlook.com address. If outlook address has to be used, maybe send the mail to gmail address and
set up automatic forwarding to outlook.

## Future possibilities

Investigate some paid trend API's, like https://explodingtopics.com.