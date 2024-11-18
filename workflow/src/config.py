from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()
HN_API_BASE = os.getenv("HN_API_BASE", "")

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
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")


# Discord webhook
HACKER_NEWS_DISCORD_WEBHOOK = os.getenv("HACKER_NEWS_DISCORD_WEBHOOK", "")

# LLM Settings
USE_AZURE_AI_API = os.getenv("USE_AZURE_AI_API", "False").lower() == "true"
USE_ANTHROPIC = os.getenv("USE_ANTHROPIC", "False").lower() == "true"
USE_OPENAI_API = os.getenv("USE_OPENAI_API", "False").lower() == "true"
USE_OPENROUTER_API = os.getenv("USE_OPENROUTER_API", "False").lower() == "true"
AZURE_MISTRAL_SMALL_API = os.getenv("AZURE_MISTRAL_SMALL_API", "")
AZURE_MISTRAL_SMALL_INFERENCE_KEY = os.getenv("AZURE_MISTRAL_SMALL_INFERENCE_KEY", "")

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

# Azure Cognitive Services
SPEECH_KEY = os.getenv("SPEECH_KEY", "")
SPEECH_REGION = os.getenv("SPEECH_REGION", "")