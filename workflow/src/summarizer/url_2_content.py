from prefect import task, flow
from src.utils.jina_reader import call_jina_reader
from src.utils.firecrawl_utils import firecrawl_scrape, firecrawl_scrape_self_hosted
from src.utils.llm_client import LLMClient
from src.utils.helpers import extract_llm_response
from src.config import (NO_CONTENT_EXTRACTED)
from .prompts import (
    EXTRACT_CONTENT_SYS_PROMPT,
    EXTRACT_CONTENT_USER_PROMPT
)
from src.common import LLMProvider
class Crawler:
    JINA_READER = "jina_reader" # default
    FIRECRAWL = "firecrawl"

class ContentExtractor:
    def __init__(self, url: str, topic: str = "", crawler: Crawler = Crawler.JINA_READER):
        self.llm_client = LLMClient(LLMProvider.AZURE_OPENAI_GPT_4o)
        self.topic = url if topic == "" else topic
        self.url = url
        self.crawler = crawler

    @task(log_prints=True, cache_policy=None)
    def extract_content(self, topic: str, content: str) -> str:
        try:
            user_input = EXTRACT_CONTENT_USER_PROMPT.format(
                JINA_READER_CONTENT=content,
                TOPIC=topic
            )
            extracted_content = self.llm_client.call_llm(
                EXTRACT_CONTENT_SYS_PROMPT,
                user_input
            )
            print(f"Extracted content preview (first 100 characters): {extracted_content[:100]}")
            return extracted_content
        except Exception as e:
            return f"Error extracting content: {e}"


    @flow(log_prints=True)
    def url_2_content(self) -> dict:
        # Fetch content
        if self.crawler == Crawler.JINA_READER:
            article, error = call_jina_reader(self.url)
        elif self.crawler == Crawler.FIRECRAWL:
            article, error = firecrawl_scrape_self_hosted(self.url)
        if error or not article:
            return { "article": error or NO_CONTENT_EXTRACTED, "title": "" }

        # Extract and process content
        article = self.extract_content(self.topic, article)
        if not article:
            return {"article": NO_CONTENT_EXTRACTED, "title": NO_CONTENT_EXTRACTED}
        title = extract_llm_response(article, "title")
        article = extract_llm_response(article, "extracted_content")
        return {"article": article, "title": title}



