from dataclasses import dataclass
from prefect import task, flow
from src.utils.llm_client import LLMClient
from src.notebooklm.app import NotebookLM
from src.summarizer.url_2_content import ContentExtractor, Crawler
from src.config import (NO_CONTENT_EXTRACTED)
from .prompts import (
    constraints_and_example,
    INITIAL_SUMMARIZE_SYSTEM_PROMPT,
    INITIAL_SUMMARIZE_USER_PROMPT,
    REFLECTION_SUMMARIZE_SYSTEM_PROMPT,
    REFLECTION_SUMMARIZE_USER_PROMPT,
    FINAL_SUMMARIZE_SYSTEM_PROMPT,
    FINAL_SUMMARIZE_USER_PROMPT,
    EXTRACT_CONTENT_SYS_PROMPT,
    EXTRACT_CONTENT_USER_PROMPT
)

@dataclass
class SummaryResult:
    initial_summary: str
    reflection: str
    final_summary: str

class ContentSummarizer:
    def __init__(self, llm_client: LLMClient, topic: str, url: str, generate_speech: bool = True, generate_podcast: bool = True, generate_summary: bool = True, content: str = "", crawler: Crawler = Crawler.JINA_READER):
        self.llm_client = llm_client
        self.topic = topic if topic != "" else url
        self.url = url
        self.content = content
        self.crawler = crawler
        self.generate_speech = generate_speech
        self.generate_podcast = generate_podcast
        self.generate_summary = generate_summary

    @task(log_prints=True, retries=2, retry_delay_seconds=[5, 10], cache_policy=None)
    def _initial_summary(self, content: str) -> str:
        print(f"initial_summary - Content preview: {content[:100]}")
        prompt = INITIAL_SUMMARIZE_USER_PROMPT.format(
            constraints_and_example=constraints_and_example, 
            tagged_text=content
        )
        summary = self.llm_client.call_llm(INITIAL_SUMMARIZE_SYSTEM_PROMPT, prompt)
        print(f"initial_summary - Summary: {summary}")
        return summary

    @task(log_prints=True, retries=2, retry_delay_seconds=[5, 10], cache_policy=None)
    def _reflection(self, content: str, summary: str) -> str:
        print(f"reflection - Content preview: {content[:100]}")
        prompt = REFLECTION_SUMMARIZE_USER_PROMPT.format(
            tagged_text=content,
            summary=summary,
            constraints_and_example=constraints_and_example
        )
        reflection = self.llm_client.call_llm(REFLECTION_SUMMARIZE_SYSTEM_PROMPT, prompt)
        print(f"reflection - Reflection: {reflection}")
        return reflection

    @task(log_prints=True, retries=2, retry_delay_seconds=[5, 10], cache_policy=None)
    def _final_summary(self, content: str, summary: str, reflection: str) -> str:
        print(f"final_summary - Content preview: {content[:100]}")
        prompt = FINAL_SUMMARIZE_USER_PROMPT.format(
            tagged_text=content,
            summary=summary,
            reflection=reflection,
            constraints_and_example=constraints_and_example
        )
        final_summary = self.llm_client.call_llm(FINAL_SUMMARIZE_SYSTEM_PROMPT, prompt)
        print(f"final_summary - Final Summary: {final_summary}")
        return final_summary

    @task(log_prints=True, cache_policy=None)
    def summarize(self, content: str) -> SummaryResult:
        print(f"Summarizing with model {self.llm_client.model}")
        print(f"Content preview: {content[:100]}")

        summary = self._initial_summary(content)
        reflection = self._reflection(content, summary)
        final_summary = self._final_summary(content, summary, reflection)

        return SummaryResult(
            initial_summary=summary,
            reflection=reflection,
            final_summary=final_summary
        )


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
    async def summarize_url(self) -> dict:
        print(f"Processing URL: {self.url} with model: {self.llm_client.model}")
        result = {"summary": "", "speech_url": "", "notebooklm_url": "", "title": ""}
        if self.content:
            article = self.content
        else:
            content_extractor = ContentExtractor(self.url, crawler=self.crawler)
            extracted_content = content_extractor.url_2_content()
            article = extracted_content.get("article", "")
            result["title"] = extracted_content.get("title", "")

        if self.generate_speech:
            audio_url = NotebookLM(self.llm_client).article_to_audio(article)
            result["speech_url"] = audio_url
        if self.generate_podcast:
            notebooklm_url = await NotebookLM(self.llm_client).generate_podcast(article)
            result["notebooklm_url"] = notebooklm_url
        if len(article) < 500:
            result["summary"] = article
            return result


        if self.generate_summary and article != NO_CONTENT_EXTRACTED:
            # Generate summary
            res = self.summarize(article)
            summary = res.final_summary.replace("\n\n", "\n")
            print(f"Initial summary: {res.initial_summary}")
            print(f"Reflection: {res.reflection}")
            print(f"Final summary: {summary}")
            result["summary"] = summary
        return result


