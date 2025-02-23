from prefect import task, flow
from src.utils.llm_client import LLMClient
from src.utils.tts import generate_podcast_audio
from src.utils.helpers import upload_file_to_r2, extract_llm_response
from .prompts import (
    SYS_PROMPT_PREPROCESS,
    SYSTEMP_PROMPT_TRANSCRIPT_WRITER,
    SYSTEMP_PROMPT_TRANSCRIPT_REWRITER
)

class NotebookLM:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        
    @task(name="preprocess_text")
    def preprocess_text(self, text: str) -> str:
        """Preprocess the raw text using LLM."""
        response = self.llm_client.call_llm(sys_prompt=SYS_PROMPT_PREPROCESS, user_input=text)
        print(f"preprocess_text - Response: {response}")
        return response

    @task(name="write_transcript")
    def write_transcript(self, preprocessed_text: str) -> str:
        """Generate podcast transcript from preprocessed text."""
        response = self.llm_client.call_llm(sys_prompt=SYSTEMP_PROMPT_TRANSCRIPT_WRITER, user_input=preprocessed_text)
        print(f"write_transcript - Response: {response}")
        return response

    @task(name="rewrite_transcript")
    def rewrite_transcript(self, transcript: str) -> str:
        """Rewrite transcript for TTS compatibility."""
        response = self.llm_client.call_llm(sys_prompt=SYSTEMP_PROMPT_TRANSCRIPT_REWRITER, user_input=transcript)
        print(f"rewrite_transcript - Response: {response}")
        response = extract_llm_response(response, "python")
        print(f"rewrite_transcript - extracted Response: {response}")
        return response

    @task(name="transcript_to_podcast")
    async def transcript_to_podcast(self, transcript: str) -> str:
        """Generate podcast audio from transcript."""
        return await generate_podcast_audio(transcript)
    
    @flow(name="generate_upload_podcast")
    async def generate_and_upload_podcast(self, raw_text: str) -> str:
        """Main flow to generate podcast from raw text."""
        preprocessed = self.preprocess_text(raw_text)
        transcript = self.write_transcript(preprocessed)
        tts_transcript = self.rewrite_transcript(transcript)
        audio_path = await self.transcript_to_podcast(tts_transcript)
        public_url = upload_file_to_r2(audio_path)
        print(f"generate_upload_podcast - Public URL: {public_url}")
        return public_url