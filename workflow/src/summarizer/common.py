from src.notebooklm.app import NotebookLM
from prefect import task
import os
import uuid
from src.config import AUDIO_CACHE_DIR
from src.utils.tts import text_to_speech
from src.utils.helpers import upload_file_to_r2

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