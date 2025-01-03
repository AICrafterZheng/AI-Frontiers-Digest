import tweepy
from src.config import TWITTER_BEARER_TOKEN, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET
from logging import getLogger

logger = getLogger(__name__)

class TwitterClient:
    def __init__(self):
        # Initialize v2 client for tweets
        self.client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token=TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        # Initialize v1 API for media upload only
        auth = tweepy.OAuth1UserHandler(
            TWITTER_CONSUMER_KEY,
            TWITTER_CONSUMER_SECRET,
            TWITTER_ACCESS_TOKEN_KEY,
            TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(auth)

    def send_tweet(self, text: str, image_path: str = None) -> None:
        """
        Send a tweet with text and an image.
        
        Args:
            text: The text content of the tweet
            image_path: Path to the image file to be uploaded (optional)
        """
        try:
            media_ids = None
            if image_path:
                # Use v1 API for media upload only
                media = self.api.media_upload(filename=image_path)
                media_ids = [media.media_id_string]
            
            # Use v2 client for creating the tweet
            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids
            )
            logger.info(f"Tweet sent successfully: {response}")
            return response
        except Exception as error:
            logger.error(f"Error sending tweet: {error}")