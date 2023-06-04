from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class YoutubeService:
    # Initialize the request
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
        self.request = self.youtube.videos().list(
            part='snippet',
            chart='mostPopular',
            maxResults=50,
            regionCode="US"
        )

    # execute the request and return the results
    def __call__(self):
        response = self.request.execute()
        print(len(self._parse_response(response["items"])))

    def _parse_response(self, response):
        recent=[]
        for video in response:
            published=datetime.strptime(video["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            if published > self._hours_ago(24):
                recent.append(video)
        return recent

    def _hours_ago(self, hours):
        return (datetime.now() - timedelta(hours=hours)) #.strftime("%Y-%m-%dT%H:%M:%SZ")


YoutubeService()()
