import tweepy
class TwitterClient:
    def __init__(self, bearer_token: str, consumer_key: str, consumer_secret: str, access_token_key: str, access_token_secret: str):
        self.client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token_key, access_token_secret=access_token_secret)

    def get_client(self):
        return self.client