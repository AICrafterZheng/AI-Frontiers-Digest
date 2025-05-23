from prefect import task, flow
from .prompts import (
    constraints_and_example,
    SIMPLE_SUMMARIZE_SYSTEM_PROMPT,
    SIMPLE_SUMMARIZE_USER_PROMPT,
    podcast_system_prompt,
    podcast_user_prompt
)
from src.config import (NO_CONTENT_EXTRACTED)
from src.summarizer.url_2_content import ContentExtractor, Crawler
from src.utils.llm_client import LLMClient
from src.utils.helpers import extract_llm_response
from src.utils.tts import article_to_audio
from src.notebooklm.app import NotebookLM
class SimpleSummarizer:
    def __init__(self, llm_client: LLMClient, topic: str, url: str, content: str = "", crawler: Crawler = Crawler.JINA_READER, generate_speech: bool = True, generate_podcast: bool = True, generate_summary: bool = True):
        self.llm_client = llm_client
        self.topic = topic if topic != "" else url
        self.url = url
        self.content = content
        self.generate_speech = generate_speech
        self.generate_podcast = generate_podcast
        self.generate_summary = generate_summary
        self.crawler = crawler


    @task(log_prints=True, cache_policy=None)
    def summarize(self, content: str, system_prompt: str = "", user_prompt: str = "") -> str:
        print(f"summarize - Content preview: {content[:100]}")
        if system_prompt == "":
            system_prompt = SIMPLE_SUMMARIZE_SYSTEM_PROMPT
        if user_prompt == "":
            user_prompt = SIMPLE_SUMMARIZE_USER_PROMPT.format(
                constraints_and_example=constraints_and_example, 
                tagged_text=content
            )
        summary = self.llm_client.call_llm(system_prompt, user_prompt)
        print(f"summarize - Summary: {summary}")
        return summary

    @flow(log_prints=True)
    async def summarize_url(self) -> dict:
        print(f"Processing URL: {self.url} with model: {self.llm_client.model}")
        result = {"summary": "", "title": ""}
        if not self.url:
            article = self.content
        else:
            # Fetch content
            content_extractor = ContentExtractor(self.url, topic=self.topic, crawler=self.crawler)
            extracted_content = content_extractor.url_2_content()
            article = extracted_content.get("article", "")
            result["title"] = extracted_content.get("title", "")

        if self.generate_speech:
            audio_url = article_to_audio(article)
            result["speech_url"] = audio_url
        if self.generate_podcast:
            notebooklm = NotebookLM(self.llm_client)
            notebooklm_url = await notebooklm.generate_podcast(article)
            result["notebooklm_url"] = notebooklm_url

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


    def summarize_content(self,  output_file: str, system_prompt: str = podcast_system_prompt) -> str:
        try:
            summary = self.llm_client.call_llm(sys_prompt=system_prompt, user_input=self.content)
            summary = extract_llm_response(summary, "blog_post")
            # Write summaries to the output file
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write(summary)
            print(f"Summary have been saved to {output_file}")
            return summary
        except Exception as e:
            print(f"Error in summarize_file: {e}")
