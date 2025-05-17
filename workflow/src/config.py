from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()
HN_API_BASE = os.getenv("HN_API_BASE", "")

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Azure OpenAI Settings
AZURE_OPENAI_API_BASE = os.getenv("AZURE_OPENAI_API_BASE", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
AZURE_OPENAI_API_GPT_4o_MINI = os.getenv("AZURE_OPENAI_API_GPT_4o_MINI", "")
AZURE_OPENAI_API_GPT_4o = os.getenv("AZURE_OPENAI_API_GPT_4o", "")
AZURE_OPENAI_API_GPT_41 = os.getenv("AZURE_OPENAI_API_GPT_41", "")
AZURE_OPENAI_API_GPT_41_KEY = os.getenv("AZURE_OPENAI_API_GPT_41_KEY", "")
AZURE_OPENAI_API_GPT41_BASE = os.getenv("AZURE_OPENAI_API_GPT41_BASE", "")

# Azure Mistral Settings
AZURE_MISTRAL_LARGE_API = os.getenv("AZURE_MISTRAL_LARGE_API", "")
AZURE_MISTRAL_LARGE_INFERENCE_KEY = os.getenv("AZURE_MISTRAL_LARGE_INFERENCE_KEY", "")
AZURE_MISTRAL_SMALL_API = os.getenv("AZURE_MISTRAL_SMALL_API", "")
AZURE_MISTRAL_SMALL_INFERENCE_KEY = os.getenv("AZURE_MISTRAL_SMALL_INFERENCE_KEY", "")

# Azure DeepSeek Settings
AZURE_DEEPSEEK_API = os.getenv("AZURE_DEEPSEEK_API", "")
AZURE_DEEPSEEK_INFERENCE_KEY = os.getenv("AZURE_DEEPSEEK_INFERENCE_KEY", "")

# OpenRouter Settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL_MISTRAL_FREE = os.getenv("OPENROUTER_MODEL_MISTRAL_FREE", "")
OPENROUTER_MODEL_LLAMA_FREE = os.getenv("OPENROUTER_MODEL_LLAMA_FREE", "")
OPENROUTER_MODEL_CLAUDE_35_SONNET = os.getenv("OPENROUTER_MODEL_CLAUDE_35_SONNET", "")
OPENROUTER_MODEL_MISTRAL_3B = os.getenv("OPENROUTER_MODEL_MISTRAL_3B", "")
OPENROUTER_MODEL_LLAMA = os.getenv("OPENROUTER_MODEL_LLAMA", "")
OPENROUTER_MODEL_MISTRAL = os.getenv("OPENROUTER_MODEL_MISTRAL", "")
OPENROUTER_MODEL_PHI_3_MINI_128K_INSTRUCT_FREE = os.getenv("OPENROUTER_MODEL_PHI_3_MINI_128K_INSTRUCT_FREE", "")

# Twitter API credentials
CONSUMER_KEY = os.getenv("CONSUMER_KEY", "")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET", "")
ACCESS_TOKEN_KEY = os.getenv("ACCESS_TOKEN_KEY", "")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET", "")

# Twitter Configuration
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", "")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", "")
TWITTER_ACCESS_TOKEN_KEY = os.getenv("TWITTER_ACCESS_TOKEN_KEY", "")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

# Discord settings
HACKER_NEWS_DISCORD_WEBHOOK = os.getenv("HACKER_NEWS_DISCORD_WEBHOOK", "")
AI_FRONTIERS_DIGEST_DISCORD_WEBHOOK = os.getenv("AI_FRONTIERS_DIGEST_DISCORD_WEBHOOK", "")
DISCORD_FOOTER = "Interested in listening to the podcast? Visit <https://aicrafter.info> 🎧"
DISCORD_SERVER_INVITE = "https://discord.gg/Ukbeb8rDmm"

# LLM Settings
USE_AZURE_AI_API = os.getenv("USE_AZURE_AI_API", "False").lower() == "true"
USE_ANTHROPIC = os.getenv("USE_ANTHROPIC", "False").lower() == "true"
USE_OPENAI_API = os.getenv("USE_OPENAI_API", "False").lower() == "true"
USE_OPENROUTER_API = os.getenv("USE_OPENROUTER_API", "False").lower() == "true"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL_MISTRAL = os.getenv("OPENROUTER_MODEL_MISTRAL", "")

# Email settings
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

# Services settings
DEFAULT_KEYWORDS = os.getenv("DEFAULT_KEYWORDS", "['gpt', 'llm', 'workflow', 'serverless']")
DEFAULT_MIN_SCORE = os.getenv("DEFAULT_MIN_SCORE", "40")
HN_SOURCE_NAME = os.getenv("HN_SOURCE_NAME", "HackerNews")
TC_SOURCE_NAME = os.getenv("TC_SOURCE_NAME", "TechCrunch")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "")
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME", "")

# TTS settings
AUDIO_CACHE_DIR = os.path.join(os.path.dirname(__file__), 'tmp', 'cache')
CACHE_DURATION = 1 * 2 * 60 * 60  # 2 hours

# Azure Cognitive Services
SPEECH_KEY = os.getenv("SPEECH_KEY", "")
SPEECH_REGION = os.getenv("SPEECH_REGION", "")
HOST_VOICE = "en-US-AvaMultilingualNeural"
# GUEST_VOICE = "en-US-BrianMultilingualNeural"
GUEST_VOICE = "en-US-AndrewMultilingualNeural"

# Cloudflare
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CLOUDFLARE_ACCESS_KEY_ID = os.getenv("CLOUDFLARE_ACCESS_KEY_ID", "")
CLOUDFLARE_ACCESS_KEY_SECRET = os.getenv("CLOUDFLARE_ACCESS_KEY_SECRET", "")
CLOUDFLARE_BUCKET_NAME = os.getenv("CLOUDFLARE_BUCKET_NAME", "")
CLOUDFLARE_AUDIO_URL = os.getenv("CLOUDFLARE_AUDIO_URL", "")

# Messages
FAILED_TO_FETCH_ARTICLE = "Jina Reader failed to fetch article"
NO_CONTENT_EXTRACTED = "Jina Reader returned no content"

# Firecrawl
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
FIRECRAWL_SELF_HOSTED_URL = os.getenv("FIRECRAWL_SELF_HOSTED_URL", "")