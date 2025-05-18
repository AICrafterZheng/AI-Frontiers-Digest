import azure.cognitiveservices.speech as speechsdk
from src.config import SPEECH_KEY, SPEECH_REGION, HOST_VOICE, GUEST_VOICE, AUDIO_CACHE_DIR
from prefect import task, get_run_logger
import asyncio
import io
import ast
import uuid
import os
from pydub import AudioSegment
from src.utils.r2_client import R2Client

@task(log_prints=True, cache_policy=None)
def article_to_audio(article: str) -> str:
    # Generate uuid for the file name
    print(f"Generating speech for article: {article[:100]}")
    if not article or len(article) < 100:
        print("Article too short to generate speech: {article}")
        return ""
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
    unique_filename = os.path.join(AUDIO_CACHE_DIR, f"{uuid.uuid4()}.mp3")
    text_to_speech(article, unique_filename)
    public_url = R2Client().upload_file_to_r2(unique_filename)
    return public_url

@task(log_prints=True, cache_policy=None)
def text_to_speech(text: str, output_file: str = "output.mp3"):
    """
    Convert text to speech and save to a file
    """
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    # The neural multilingual voice can speak different languages based on the input text.
    speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    # Get text from the console and synthesize to the default speaker.
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
        print("Speach path: {output_file}")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


async def generate_audio_segment(text: str, voice: str) -> str:
    logger = get_run_logger()
    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_synthesis_voice_name = voice

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        future =await asyncio.to_thread(synthesizer.speak_text_async, text)
        result = await asyncio.to_thread(future.get)
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
            audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
            return audio_segment
        else:
            logger.error(f"Speech synthesis text: {text} failed, reason: {result.reason}")
            if hasattr(result, 'cancellation_details'):
                logger.error(f"Cancellation details: {result.cancellation_details.reason}")
                logger.error(f"Cancellation error details: {result.cancellation_details.error_details}")
            return None
    except Exception as e:
        logger.error(f"Error in generate_audio_segment: {e}")

@task(name="process_lines", log_prints=True)
async def process_lines(text , host_voice, guest_voice, max_concurrency):
    semaphore = asyncio.Semaphore(max_concurrency)
    async def process_line(speaker, line):
        async with semaphore:
            voice = host_voice if speaker == 'Speaker 1' else guest_voice
            return await generate_audio_segment(line, voice )
    tasks = [process_line(speaker, line) for speaker, line in ast.literal_eval(text)]
    results = await asyncio.gather(*tasks)
    return results

@task(name="generate_podcast_audio", log_prints=True)
async def generate_podcast_audio(text: str) -> str:
    logger = get_run_logger()
    try:
        print("Starting audio generation...")
        audio_segments = await process_lines(text, HOST_VOICE, GUEST_VOICE, 3)
        print("Audio generation completed")
        # Filter out None values if any audio generation failed
        audio_segments = [seg for seg in audio_segments if seg is not None]
        if not audio_segments:
            logger.error("No audio segments were generated successfully")
            return None
        combined_audio = await asyncio.to_thread(sum, audio_segments)
        print("Audio combined")
        os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
        unique_filename = os.path.join(AUDIO_CACHE_DIR, f"{uuid.uuid4()}.mp3")
        await asyncio.to_thread(combined_audio.export, unique_filename, format="mp3")
        return unique_filename
    except Exception as e:
        logger.error(f"Error in generate_podcast_audio: {e}")
