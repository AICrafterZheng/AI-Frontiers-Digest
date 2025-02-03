from dataclasses import dataclass
from prefect import task, flow
from src.utils.jina_reader import call_jina_reader
from src.utils.llm_client import LLMClient
from src.utils.helpers import extract_llm_response
from src.utils.tts import text_to_speech
from src.utils.helpers import upload_file_to_r2
from src.notebooklm.app import NotebookLM
import uuid
from src.config import (AUDIO_CACHE_DIR, 
                        NO_CONTENT_EXTRACTED)
import os
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
    def __init__(self, llm_client: LLMClient, topic: str, url: str, generate_speech: bool = True, generate_podcast: bool = True, generate_summary: bool = True, content: str = ""):
        self.llm_client = llm_client
        self.topic = topic if topic != "" else url
        self.url = url
        self.content = content
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

    @task(log_prints=True, cache_policy=None)
    def article_to_speech(self, article: str) -> str:
        # Generate uuid for the file name
        print(f"Generating speech for article: {self.url}")
        os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
        unique_filename = os.path.join(AUDIO_CACHE_DIR, f"{uuid.uuid4()}.mp3")
        text_to_speech(article, unique_filename)
        public_url = upload_file_to_r2(unique_filename)
        return public_url

    @task(log_prints=True, cache_policy=None)
    async def article_to_podcast(self, article: str) -> str:
        print(f"Generating podcast for article: {self.url}")
        if not article or len(article) < 100:
            print("Article too short to generate podcast: {article}")
            return ""
        notebooklm = NotebookLM(llm_client=self.llm_client)
        public_url = await notebooklm.generate_and_upload_podcast(article)
        return public_url

    @flow(log_prints=True)
    def extract_content_from_url(self) -> dict:
        # Fetch content
        article, error = call_jina_reader(self.url)
        if error or not article:
            return { "article": error or NO_CONTENT_EXTRACTED, "title": "" }

        # Extract and process content
        article = self.extract_content(self.topic, article)
        if not article:
            return {"article": NO_CONTENT_EXTRACTED, "title": NO_CONTENT_EXTRACTED}
        title = extract_llm_response(article, "title")
        article = extract_llm_response(article, "extracted_content")

        return {"article": article, "title": title}


    @flow(log_prints=True)
    async def summarize_url(self) -> dict:
        print(f"Processing URL: {self.url} with model: {self.llm_client.model}")
        result = {"summary": "", "speech_url": "", "notebooklm_url": "", "title": ""}
        if self.content:
            article = self.content
        else:
            extracted_content = self.extract_content_from_url()
            article = extracted_content.get("article", "")
            result["title"] = extracted_content.get("title", "")

        if self.generate_speech:
            audio_url = self.article_to_speech(article)
            result["speech_url"] = audio_url
        if self.generate_podcast:
            notebooklm_url = await self.article_to_podcast(article)
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


