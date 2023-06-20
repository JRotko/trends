import tweepy
import os
from dotenv import load_dotenv
load_dotenv()



trends = [
  {
    "trends": [
      {
        "name": "#Coke",

      },
      {
        "name": "#Bloat",
      },
      {
        "name": "#Celsius"
      },
      {
        "name": "#COD4"
      },
      {
        "name": "#KTM"
      }
    ]
  }
]

class Twitter:
    def __init__(self):
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def __call__(self):
        # WOEID of US
        # https://gist.github.com/tedyblood/5bb5a9f78314cc1f478b3dd7cde790b9
        woeid = 12

        # fetching the trends
        # trends = api.get_place_trends(id = woeid)

        messages = []
        for trend in trends[0]['trends']:
            prompt = f'{trend["name"]}'
            messages.append({"role": "user", "content": prompt})

        if messages:
            messages.insert(0, {"role": "system", "content": open('twitter_instruction.txt', 'r').read()})
            return messages
        return False

    def trends_sample(self):
        return [
                    {
                        "trends": [
                        {
                            "name": "#Coke",
                            "url": "http://twitter.com/search?q=%23TrendingHashtag1",
                            "promoted_content": "null",
                            "query": "%23TrendingHashtag1",
                            "tweet_volume": 12345
                        },
                        {
                            "name": "#Bloat",
                            "url": "http://twitter.com/search?q=%23TrendingHashtag2",
                            "promoted_content": "null",
                            "query": "%23TrendingHashtag2",
                            "tweet_volume": 67890
                        },
                        ]
                    }
                ]

Twitter()()

