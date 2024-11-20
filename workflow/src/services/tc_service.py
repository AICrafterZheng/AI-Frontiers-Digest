import requests
from prefect import task, flow, get_run_logger
from prefect.variables import Variable
import re
from datetime import datetime
from src.utils.discord import split_messages_to_send_discord
from src.summarizer.agentic_summarizer import ContentSummarizer
from urllib.parse import urlparse
import pytz
from typing import List
from src.utils.llm_client import LLMClient
from src.services.models import Story
from src.utils.email_templates import get_tc_email_template
from src.utils.email_sender import send_emails
from src.config import HACKER_NEWS_DISCORD_WEBHOOK, TC_SOURCE_NAME, AI_FRONTIERS_DIGEST_DISCORD_WEBHOOK
from src.utils.helpers import save_to_supabase

class TechCrunchService:
    def __init__(self):
        self.base_url = "https://techcrunch.com/category/artificial-intelligence/"
        self.llm_client = LLMClient(use_azure_mistral=True, model="large")
        self.header = "AI Frontiers on TechCrunch"
        self.formatted_date = datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y/%m/%d")
        self.discord_webhooks = []
    @classmethod
    async def create(cls):
        instance = cls()
        discord_webhook = await Variable.get("discord_webhook", "")
        instance.discord_webhooks.append(HACKER_NEWS_DISCORD_WEBHOOK if discord_webhook == "" else discord_webhook)
        instance.discord_webhooks.append(AI_FRONTIERS_DIGEST_DISCORD_WEBHOOK)
        return instance
    
    def is_image_url(self, url: str) -> bool:
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        parsed_url = urlparse(url)
        if any(parsed_url.path.lower().endswith(ext) for ext in image_extensions):
            return True
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            content_type = response.headers.get('Content-Type', '')
            return content_type.startswith('image/')
        except requests.RequestException:
            return False

    @task(log_prints=True, cache_key_fn=None)
    def get_ai_urls_from_tc(self) -> List[str]:
        response = requests.get(self.base_url)
        input_text = response.text
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = re.findall(url_pattern, input_text)
        urls = [url for url in urls if self.formatted_date in url and not self.is_image_url(url)]
        urls = list(set(urls))
        print(f"Found {len(urls)} URLs: \n{urls}")
        return urls

    def process_urls(self, urls: List[str]) -> List[Story]:
        first_news = True
        stories = []
        
        for url in urls:
            # Use TechCrunch url as the topic
            result = ContentSummarizer(self.llm_client, url, url).summarize_url()
            summary = result.get("summary")
            speech_url = result.get("speech_url")
            if summary and summary != "No relevant content found":
                title = summary.split("\n")[0]
                title = title.strip('"').strip('(').strip(')').strip("'")
                stories.append(Story(url=url, title=title, summary=summary, source=TC_SOURCE_NAME, speech_url=speech_url))
            if first_news:
                message = f"{self.header}\n<{url}>\n{summary}"
                first_news = False
            else:
                message = f"\n<{url}>\n{summary}"
            message = message.replace("\n\n", "\n")
            for webhook in self.discord_webhooks:
                split_messages_to_send_discord(webhook, message)
        return stories

    @task
    async def send_newsletter(self, stories: List[Story], to_emails: List[str] = None) -> None:
        """Send email newsletter"""
        logger = get_run_logger()
        try:
            message = get_tc_email_template(self.header, stories)
            await send_emails(self.header, message, to_emails)
        except Exception as e:
            logger.error(f"Error sending emails: {e}")

    async def run_flow(self):
        print(f"Formatted date: {self.formatted_date}")
        urls = self.get_ai_urls_from_tc()
        stories = self.process_urls(urls)
        await self.send_newsletter(stories)
        save_to_supabase(stories)


@flow(log_prints=True, name="tc-summary-flow")
async def run_tc_flow():
    service = await TechCrunchService.create()
    await service.run_flow()

@flow(log_prints=True, name="test-flow")
async def run_test_tc_flow():
    urls = ["https://www.latent.space/p/ai-ux-moat"]  
    service = await TechCrunchService.create()
    service.formatted_date = "2024/11/08"
    service.discord_webhooks = [HACKER_NEWS_DISCORD_WEBHOOK]
    stories = service.process_urls(urls)
    await service.send_newsletter(stories, to_emails=["aicrafter.ai@gmail.com"])
    save_to_supabase(stories)
