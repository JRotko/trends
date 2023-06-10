from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class YoutubePopularFinder:
    # Initialize the request
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))


    # execute the request and return the results
    def __call__(self):
        videos = self._get_videos(self.youtube)
        return self._find_recent_videos(videos)

    def _find_recent_videos(self, videos, hours=24):
        recent=[]
        for video in videos:
            published=datetime.strptime(video["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            if published > self._hours_ago(hours):
                recent.append(video)
        return recent

    def _hours_ago(self, hours):
        return (datetime.now() - timedelta(hours=hours)) #.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _get_videos(self, youtube, max_results=200):
        videos = []
        request = youtube.videos().list(
            part='snippet',
            chart='mostPopular',
            regionCode='US',
            maxResults=50
        )

        while len(videos) < max_results:
            response = request.execute()
            videos.extend(response['items'])

            # If there's no next page, we're done.
            if 'nextPageToken' not in response:
                break

            # Otherwise, set up the next request.
            request = youtube.videos().list(
                part='snippet',
                chart='mostPopular',
                regionCode='US',
                maxResults=50,
                pageToken=response['nextPageToken']
            )

        return videos



YoutubePopularFinder()()
