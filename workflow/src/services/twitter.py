from typing import List, Optional
import tweepy
from prefect import task, flow, get_run_logger
from prefect.variables import Variable
from datetime import datetime, timedelta
import asyncio
from src.config import TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET
from .models import Story
from src.utils.jina_reader import call_jina_reader

class TwitterService:
    def __init__(self):
        self.logger = get_run_logger()
        self.client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            wait_on_rate_limit=True
        )
        self.source = "Twitter"

    @classmethod
    async def create(cls):
        instance = cls()
        # Get Twitter usernames from Prefect variables
        instance.usernames = await Variable.get("twitter_usernames", "")
        instance.usernames = [
            "karpathy",
            "sama",
            "ylecun",
            "_jasonwei",
            "jimfan",
            "DrJimFan",
        ] if instance.usernames == "" else instance.usernames.split(",")
        return instance

    async def get_user_ids(self) -> List[str]:
        """Get Twitter user IDs from usernames."""
        user_ids = []
        for username in self.usernames:
            try:
                user = self.client.get_user(username=username)
                if user.data:
                    user_ids.append(user.data.id)
            except Exception as e:
                self.logger.error(f"Error getting user ID for {username}: {e}")
        return user_ids

    async def get_tweets(self, user_id: str, start_time: Optional[datetime] = None) -> List[dict]:
        """Get tweets from a user."""
        try:
            # Get tweets from the last 24 hours if no start_time provided
            if not start_time:
                start_time = datetime.utcnow() - timedelta(days=1)

            tweets = self.client.get_users_tweets(
                user_id,
                max_results=10,
                start_time=start_time,
                tweet_fields=['created_at', 'public_metrics', 'entities'],
                exclude=['retweets', 'replies']
            )
            if not tweets.data:
                return []

            return [{
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'metrics': tweet.public_metrics,
                'urls': [url['expanded_url'] for url in tweet.entities.get('urls', [])] if tweet.entities else []
            } for tweet in tweets.data]

        except Exception as e:
            self.logger.error(f"Error getting tweets for user {user_id}: {e}")
            return []

    @task(log_prints=True, name="process-tweets", cache_policy=None)
    async def process_tweets(self) -> List[Story]:
        """Process tweets and extract relevant content."""
        stories = []
        user_ids = await self.get_user_ids()

        for user_id in user_ids:
            tweets = await self.get_tweets(user_id)
            for tweet in tweets:
                # Process each URL in the tweet
                for url in tweet['urls']:
                    try:
                        if not url or 'twitter.com' in url:
                            continue

                        content = call_jina_reader(url)
                        if not content:
                            continue

                        story = Story(
                            id=str(tweet['id']),
                            title=tweet['text'][:100] + "...",  # Use first 100 chars as title
                            url=url,
                            score=tweet['metrics']['like_count'],
                            source=self.source,
                            content=content
                        )
                        stories.append(story)

                    except Exception as e:
                        self.logger.error(f"Error processing tweet {tweet['id']}: {e}")
                        continue

        return stories

@flow(name="twitter-flow")
async def run_twitter_flow():
    """Main flow to process Twitter content."""
    service = await TwitterService.create()
    service.usernames = ["karpathy"]
    stories = await service.process_tweets()
    print(f"Found {len(stories)} stories")
    print(stories)
    return stories

if __name__ == "__main__":
    asyncio.run(run_twitter_flow())
