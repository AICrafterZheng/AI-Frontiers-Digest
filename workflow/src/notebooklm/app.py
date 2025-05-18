from prefect import task, flow
from src.utils.llm_client import LLMClient
from src.utils.tts import generate_podcast_audio
from src.utils.helpers import extract_llm_response
from src.utils.r2_client import R2Client
from .prompts import (
    SYS_PROMPT_PREPROCESS,
    SYSTEMP_PROMPT_TRANSCRIPT_WRITER,
    SYSTEMP_PROMPT_TRANSCRIPT_REWRITER,
    chinese_podcast_prompt,
    one_shot_transcript_prompt
)
from src.utils.llm_client import LLMProvider
class NotebookLM:
    def __init__(self, llm_client: LLMClient = None):
        self.llm_client = llm_client if llm_client is not None else LLMClient(LLMProvider.AZURE_OPENAI_GPT_4o_MINI)
        
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

    @task(name="generate_chinese_podcast")
    def generate_chinese_podcast(self, raw_text: str) -> str:
        """Generate Chinese podcast from raw text."""
        response = self.llm_client.call_llm(sys_prompt=chinese_podcast_prompt, user_input=raw_text)
        print(f"generate_chinese_podcast - Response: {response}")
        return response

    def one_shot_transcript(self, raw_text: str) -> str:
        """Generate one shot transcript from raw text."""
        response = self.llm_client.call_llm(sys_prompt=one_shot_transcript_prompt, user_input=raw_text)
        print(f"one_shot_transcript - Prompt: {one_shot_transcript_prompt[:100]}")
        print(f"one_shot_transcript - Response: {response}")
        return response

    @task(name="transcript_to_podcast")
    async def transcript_to_podcast(self, transcript: str) -> str:
        """Generate podcast audio from transcript."""
        return await generate_podcast_audio(transcript)
    
    @flow(name="generate_podcast")
    async def generate_podcast(self, raw_text: str) -> str:
        """Main flow to generate podcast from raw text."""
        print(f"Generating podcast for text: {raw_text[:100]}")
        if not raw_text or len(raw_text) < 100:
            print("Text too short to generate podcast: {raw_text}")
            return ""
        # preprocessed = self.preprocess_text(raw_text)
        # transcript = self.write_transcript(preprocessed)
        # tts_transcript = self.rewrite_transcript(transcript)
        one_shot_transcript = self.one_shot_transcript(raw_text)
        audio_path = await self.transcript_to_podcast(one_shot_transcript)
        public_url = R2Client().upload_file_to_r2(audio_path)
        print(f"generate_podcast - Public URL: {public_url}")
        return public_url
    # test flow
    @flow(name="test_generate_chinese_podcast")
    async def test_generate_chinese_podcast(self, raw_text: str):
        """Test flow to generate Chinese podcast."""
        response = self.one_shot_transcript(raw_text)
        audio_path = await self.transcript_to_podcast(response)
        print(f"test_generate_chinese_podcast - Audio path: {audio_path}")

