import requests
from prefect import task, flow, get_run_logger
from prefect.variables import Variable
import re
from datetime import datetime, timedelta
from src.utils.discord import split_messages_to_send_discord
from src.summarizer.agentic_summarizer import ContentSummarizer
from urllib.parse import urlparse
import pytz
from typing import List
from src.utils.llm_client import LLMClient
from src.services.models import Story
from src.utils.email_templates import get_email_html
from src.utils.email_sender import send_emails
from src.config import HACKER_NEWS_DISCORD_WEBHOOK, TC_SOURCE_NAME, AI_FRONTIERS_DIGEST_DISCORD_WEBHOOK, DISCORD_FOOTER
from src.utils.helpers import save_to_supabase, update_supabase_row
from src.utils.supabase_utils import checkIfExists
import time
class TechCrunchService:
    def __init__(self):
        self.base_url = "https://techcrunch.com/category/artificial-intelligence/"
        self.llm_client = LLMClient(use_azure_mistral=True, model="large")
        self.header = "AI Frontiers on TechCrunch"
        
        # Get current date in PST
        today = datetime.now(pytz.timezone('America/Los_Angeles'))
        # Get yesterday's date
        yesterday = today - timedelta(days=1)
        # Format both dates
        self.formatted_dates = [
            today.strftime("%Y/%m/%d"),
            yesterday.strftime("%Y/%m/%d")
        ]
        self.discord_webhooks = []
        self.columns_to_update = []
        self.save_to_supabase = True
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

    def check_if_exists_in_supabase(self, url: str) -> bool:
        return checkIfExists('url', url)

    @task(log_prints=True, cache_policy=None)
    def get_ai_urls_from_tc(self) -> List[str]:
        response = requests.get(self.base_url)
        input_text = response.text
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = re.findall(url_pattern, input_text)
        urls = [
            url for url in urls 
            if any(date in url for date in self.formatted_dates) 
            and not self.is_image_url(url) 
            and not self.check_if_exists_in_supabase(url)
        ]
        urls = list(set(urls))
        print(f"Found {len(urls)} URLs: \n{urls}")
        return urls

    async def process_urls(self, urls: List[str]) -> List[Story]:
        first_news = True
        stories = []
        for url in urls:
            # Use TechCrunch url as the topic
            result = await ContentSummarizer(
                llm_client=self.llm_client, 
                topic=url, 
                url=url, 
                generate_summary= len(self.columns_to_update) == 0 or "summary" in self.columns_to_update,
                generate_speech= len(self.columns_to_update) == 0 or "speech_url" in self.columns_to_update,
                generate_podcast= len(self.columns_to_update) == 0 or "notebooklm_url" in self.columns_to_update
            ).summarize_url()
            summary = result.get("summary")
            speech_url = result.get("speech_url")
            notebooklm_url = result.get("notebooklm_url")
            if (summary and summary != "No relevant content found") or len(self.columns_to_update) > 0:
                title = summary.split("\n")[0]
                title = title.strip('"').strip('(').strip(')').strip("'")
                id = int(time.time())
                story = Story(id=id, url=url, title=title, summary=summary, source=TC_SOURCE_NAME, speech_url=speech_url, notebooklm_url=notebooklm_url)
                stories.append(story) # for later email sending
                # save to supabase
                if self.save_to_supabase:
                    save_to_supabase([story])
            if first_news:
                message = f"{self.header}\n<{url}>\n{summary}"
                first_news = False
            else:
                message = f"\n<{url}>\n{summary}"
            message = message.replace("\n\n", "\n")
            # send to discord
            for webhook in self.discord_webhooks: 
                split_messages_to_send_discord(webhook, message)
            

        if len(stories) > 0: # send footer
            for webhook in self.discord_webhooks:
                split_messages_to_send_discord(webhook, DISCORD_FOOTER)
        return stories

    @task(log_prints=True, cache_policy=None)
    async def send_emails(self, stories: List[Story], to_emails: List[str] = None) -> None:
        """Send email newsletter"""
        logger = get_run_logger()
        try:
            message = get_email_html(self.header, stories)
            await send_emails(self.header, message, to_emails)
        except Exception as e:
            logger.error(f"Error sending emails: {e}")

    async def run_flow(self):
        print(f"Formatted date: {self.formatted_dates}")
        urls = self.get_ai_urls_from_tc()
        stories = await self.process_urls(urls)
        await self.send_emails(stories)

@flow(log_prints=True, name="tc-flow")
async def run_tc_flow():
    service = await TechCrunchService.create()
    await service.run_flow()

@flow(log_prints=True, name="test-tc-flow")
async def run_test_tc_flow():
    # urls = ["https://techcrunch.com/2024/11/23/meet-three-incoming-eu-lawmakers-in-charge-of-key-tech-policy-areas/"]

    from src.utils.supabase_utils import searchRow
    from src.config import SUPABASE_TABLE
    stories = searchRow(SUPABASE_TABLE, "source", TC_SOURCE_NAME, "speech_url", None)
    urls = [story["url"] for story in stories]
    print(f"len: {len(urls)}")
    # urls = urls[:20]
    
    service = await TechCrunchService.create()
    service.save_to_supabase = False
    columns_to_update = []
    # columns_to_update.append("summary")
    columns_to_update.append("speech_url") 
    # columns_to_update.append("notebooklm_url")
    columns_to_update.append("story_id")
    service.columns_to_update = columns_to_update
    service.formatted_dates = ["2024/11/19", "2024/11/20"]
    # urls = service.get_ai_urls_from_tc()
    service.discord_webhooks = []
    stories = await service.process_urls(urls)
    print(f"processed {len(stories)} stories")
    # await service.send_emails(stories, to_emails=["aicrafter.ai@gmail.com"])
    # save_to_supabase(stories)
    update_supabase_row(stories, "url", columns_to_update)