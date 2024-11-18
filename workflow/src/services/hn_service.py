from typing import List
import aiohttp
import asyncio
from prefect import flow, task, get_run_logger
from prefect.variables import Variable
from prefect.artifacts import create_table_artifact
from src.utils.email_templates import get_hn_email_template
from src.utils.llm_client import LLMClient
from src.utils.email_sender import send_emails
from src.utils.supabase_utils import checkIfExists
from src.summarizer.hn_comments_summarizer import HNCommentsSummarizer
from src.summarizer.agentic_summarizer import ContentSummarizer
from src.utils.discord import send_discord
from src.utils.helpers import has_mentioned_keywords, save_to_supabase

from src.config import (
    HN_API_BASE,
    HACKER_NEWS_DISCORD_WEBHOOK,
    HN_SOURCE_NAME
)
from .models import Story


class HackerNewsService:
    def __init__(self):
        self.logger = get_run_logger()
        self.header = "AI Frontiers on Hacker News"
        self.llm_client = LLMClient(use_azure=True)
        
    @classmethod
    async def create(cls):
        instance = cls()
        # Move async initialization here
        instance.discord_keywords = await Variable.get("discord_keywords", "")
        instance.discord_keywords = ['gpt', ' llm', ' workflow', ' serverless'] if instance.discord_keywords == "" else instance.discord_keywords.split(",")
        
        instance.score = await Variable.get("score", "")
        instance.score = 40 if instance.score == "" else int(instance.score)
        
        instance.discord_webhook = await Variable.get("discord_webhook", "")
        instance.discord_webhook = HACKER_NEWS_DISCORD_WEBHOOK if instance.discord_webhook == "" else instance.discord_webhook
        return instance

    @task(log_prints=True)
    async def fetchTopStoryIds(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{HN_API_BASE}/topstories.json") as response:
                data = await response.json()
        return data

    # Check if new and mentioned in keywords
    @task(log_prints=True, name="top-hn-processStories")
    async def processStories(self, stories):
        results = []
        async def processStory(id):
            # Check if story exists
            if checkIfExists(id):
                print(f"Story {id} already exists")
                return
            story = await self.fetchStory(id)
            print(f"Fetched story: {story}")
            if story is None:
                return
            # If any keywords are mentioned in the story title
            if has_mentioned_keywords(story, self.discord_keywords) and int(story.score) > self.score:
                print(f"Found a story: {story.title}, url: {story.url}")
                results.append(story)
            else:
                print(f"Story {story.title} does not have mentioned keywords {self.discord_keywords} or score is less than {self.score}")
        tasks = [processStory(id) for id in stories]
        await asyncio.gather(*tasks)
        return results

    async def fetchStory(self, id) -> Story:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{HN_API_BASE}/item/{id}.json") as response:
                data = await response.json()
                # print(f"fetchStory story: {data}")
                if 'url' in data:
                    return Story(id=id, title=data['title'], url=data['url'], score=int(data['score']), hn_url=f"https://news.ycombinator.com/item?id={id}", source=HN_SOURCE_NAME)
                else:
                    return None

    @task(log_prints=True)
    async def send_emails(self, stories, to_emails: List[str] = None):
        logger = get_run_logger()
        try:
            message = get_hn_email_template(self.header, stories)
            await send_emails(self.header, message, to_emails)
        except Exception as e:
            logger.error(f"Error sending emails: {e}")

    @task(log_prints=True)
    async def top_hn_flow(self, storieIds: list[str]):
        logger = get_run_logger()
        stories = await self.processStories(storieIds)
        print(f"Found {len(stories)} stories")
        if len(stories) == 0:
            logger.warning("No stories found")
            return stories
        # order by score in descending order
        stories = sorted(stories, key=lambda x: x.score, reverse=True)

        first_news = True
        for story in stories:
            try:
                url = story.url
                comments_summary = await HNCommentsSummarizer(self.llm_client).summarize_comments(str(story.id))
                story.comments_summary = comments_summary
                summary = ContentSummarizer(self.llm_client, story.title, url).summarize_url()
                story.summary = summary
                summary_message = f"**Article**: <{story.url}>\n**Summary**:\n {summary}"
                comments_summary_message = f"**HNUrl**: <{story.hn_url}>\n**Score**: {story.score}\n**Discussion Highlights**:\n {comments_summary}"
                logger.info(f"Story comments summary: {comments_summary_message}")
                if first_news: # add the header
                    summary_message = f"Top Hacker News:\n{summary_message}"
                    first_news = False
                send_discord(self.discord_webhook, summary_message, divider_style="none")
                send_discord(self.discord_webhook, comments_summary_message)
            except Exception as e:
                logger.error(f"Error processing story {story.title}: {e}")
        return stories

    async def run_flow(self):
        storieIds = await self.fetchTopStoryIds()
        print(f"Found {len(storieIds)} story IDs")
        stories = await self.top_hn_flow(storieIds)
        await self.send_emails(stories)
        save_to_supabase(stories)


@flow(log_prints=True, name="hn-summary-flow")
async def run_hn_flow():
    service = await HackerNewsService.create()
    await service.run_flow()

@flow(log_prints=True, name="test-flow")
async def run_test_hn_flow():
    service = await HackerNewsService.create()
    service.discord_webhook = HACKER_NEWS_DISCORD_WEBHOOK
    # service.discord_keywords = ['Y']
    # service.score = 0
    # ids = ["1"]
    storieIds = await service.fetchTopStoryIds()
    stories = await service.top_hn_flow(storieIds)
    print(f"Found {len(stories)} stories")
    await service.send_emails(stories, ["aicrafter.ai@gmail.com"])
    save_to_supabase(stories)
