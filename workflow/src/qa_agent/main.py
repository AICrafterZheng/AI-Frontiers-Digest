from utils.llm_client import LLMClient
from .prompts import SYS_PROMPT
if __name__ == "__main__":
    llm_client = LLMClient(use_azure_openai=True, model=AZURE_OPENAI_API_GPT_4o)
    image_path = "file:///Users/danny/Desktop/ai_crafter.png"
    llm_client.call_llm(SYS_PROMPT, "Create test cases for the webpage", image_path)
