from prefect import task, flow
from .prompts import (
    constraints_and_example,
    SIMPLE_SUMMARIZE_SYSTEM_PROMPT,
    SIMPLE_SUMMARIZE_USER_PROMPT
)
from src.config import (NO_CONTENT_EXTRACTED)
from .url_2_content import ContentExtractor
from src.utils.llm_client import LLMClient

class SimpleSummarizer:
    def __init__(self, llm_client: LLMClient, url: str, content: str, generate_speech: bool = True, generate_podcast: bool = True, generate_summary: bool = True):
        self.llm_client = llm_client
        self.url = url
        self.content = content
        self.generate_speech = generate_speech
        self.generate_podcast = generate_podcast
        self.generate_summary = generate_summary


    @task(log_prints=True, cache_policy=None)
    def summarize(self, content: str) -> str:
        print(f"summarize - Content preview: {content[:100]}")
        prompt = SIMPLE_SUMMARIZE_USER_PROMPT.format(
            constraints_and_example=constraints_and_example, 
            tagged_text=content
        )
        summary = self.llm_client.call_llm(SIMPLE_SUMMARIZE_SYSTEM_PROMPT, prompt)
        print(f"summarize - Summary: {summary}")
        return summary

    @flow(log_prints=True)
    def summarize_url(self) -> dict:
        print(f"Processing URL: {self.url} with model: {self.llm_client.model}")
        result = {"summary": "", "title": ""}
        if not self.url:
            article = self.content
        else:
            # Fetch content
            content_extractor = ContentExtractor(self.url)
            extracted_content = content_extractor.url_2_content()
            article = extracted_content.get("article", "")
            result["title"] = extracted_content.get("title", "")

        if len(article) < 500:
            result["summary"] = article
            return result

        if self.generate_summary and article != NO_CONTENT_EXTRACTED:
            # Generate summary
            res = self.summarize(article)
            summary = res.replace("\n\n", "\n")
            print(f"Summary: {summary}")
            result["summary"] = summary
        return result


