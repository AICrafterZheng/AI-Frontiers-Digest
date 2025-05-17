from prefect import task, flow
from .prompts import (
    constraints_and_example,
    SIMPLE_SUMMARIZE_SYSTEM_PROMPT,
    SIMPLE_SUMMARIZE_USER_PROMPT,
    podcast_system_prompt,
    podcast_user_prompt
)
from src.config import (NO_CONTENT_EXTRACTED)
from .url_2_content import ContentExtractor
from src.utils.llm_client import LLMClient
from src.utils.helpers import extract_llm_response

class SimpleSummarizer:
    def __init__(self, llm_client: LLMClient, url: str, content: str, generate_speech: bool = True, generate_podcast: bool = True, generate_summary: bool = True):
        self.llm_client = llm_client
        self.url = url
        self.content = content
        self.generate_speech = generate_speech
        self.generate_podcast = generate_podcast
        self.generate_summary = generate_summary


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
