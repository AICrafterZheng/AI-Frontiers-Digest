from dataclasses import dataclass
from prefect import task, flow
from src.utils.jina_reader import call_jina_reader
from src.utils.llm_client import LLMClient
from src.utils.helpers import extract_llm_response
from src.utils.tts import text_to_speech
from src.utils.supabase_utils import upload_audio_file
import uuid
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
    def __init__(self, llm_client: LLMClient, topic: str, url: str):
        self.llm_client = llm_client
        self.topic = topic
        self.url = url

    @task(log_prints=True, retries=2, retry_delay_seconds=[5, 10])
    def _initial_summary(self, content: str) -> str:
        print(f"initial_summary - Content preview: {content[:100]}")
        prompt = INITIAL_SUMMARIZE_USER_PROMPT.format(
            constraints_and_example=constraints_and_example, 
            tagged_text=content
        )
        summary = self.llm_client.call_llm(INITIAL_SUMMARIZE_SYSTEM_PROMPT, prompt)
        print(f"initial_summary - Summary: {summary}")
        return summary

    @task(log_prints=True, retries=2, retry_delay_seconds=[5, 10])
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

    @task(log_prints=True, retries=2, retry_delay_seconds=[5, 10])
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

    @task(log_prints=True, cache_key_fn=None)
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


    @task(log_prints=True, cache_key_fn=None)
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
            print(f"Extracted content preview: {extracted_content[:100]}")
            return extracted_content
        except Exception as e:
            return f"Error extracting content: {e}"

    @task(log_prints=True, cache_key_fn=None)
    def article_to_speech(self, article: str) -> str:
        # Generate uuid for the file name
        print(f"Generating speech for article: {self.url}")
        file_name = str(uuid.uuid4()) + ".wav"
        text_to_speech(article, file_name)
        public_url = upload_audio_file(file_name)
        return public_url
    
    @flow(log_prints=True)
    def summarize_url(self) -> dict:
        print(f"Processing URL: {self.url} with model: {self.llm_client.model}")
        result = {"summary": "", "speech_url": ""}
        # Fetch content
        article, error = call_jina_reader(self.url)
        if error or not article:
            result["summary"] = error or "Failed to fetch article"
            return result

        # Extract and process content
        article = self.extract_content(self.topic, article)
        article = extract_llm_response(article, "extracted_content")
        
        if not article:
            result["summary"] = "No content extracted"
            return result

        public_url = self.article_to_speech(article)

        if len(article) < 1000:
            result["summary"] = article
            result["speech_url"] = public_url
            return result

        # Generate summary
        res = self.summarize(article)
        summary = res.final_summary.replace("\n\n", "\n")

        print(f"Initial summary: {res.initial_summary}")
        print(f"Reflection: {res.reflection}")
        print(f"Final summary: {summary}")

        result["summary"] = summary
        result["speech_url"] = public_url
        return result


