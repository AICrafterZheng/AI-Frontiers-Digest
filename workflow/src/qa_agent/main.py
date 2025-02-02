from src.utils.llm_client import LLMClient
from .prompts import SS_TO_DESCRIPTION, SYS_PROMPT_JSON_V2, SYS_PROMPT, ECOMMERCE_PROMPT, get_ecommerce_prompt
from src.utils.helpers import extract_llm_response
from src.common import LLMProvider
import time

def gen_test_cases(web_desc: str, image_paths: list[str], description: str = ""):
    llm_client = LLMClient(LLMProvider.AZURE_OPENAI_API_GPT_4o)
    user_input = SYS_PROMPT_JSON_V2.format(description=web_desc)
    response = llm_client.call_llm(SYS_PROMPT, user_input, image_paths)
    md = extract_llm_response(response, "test_cases")
    save_test_cases_to_file(md, description)
    print("response \n", response)


def gen_test_cases_with_image(image_paths: list[str], description: str = ""):
    llm_client = LLMClient(LLMProvider.AZURE_OPENAI_API_GPT_4o)
    user_input = ECOMMERCE_PROMPT
    response = llm_client.call_llm(SYS_PROMPT, user_input, image_paths)
    md = extract_llm_response(response, "test_cases")
    save_test_cases_to_file(md, description)

def screenshot_to_description(image_path: str):
    llm_client = LLMClient(LLMProvider.AZURE_OPENAI_API_GPT_4o)
    response = llm_client.call_llm(SS_TO_DESCRIPTION, "Describe the screenshot", [image_path])
    return extract_llm_response(response, "webpage_description")


def save_test_cases_to_file(test_cases: str, file_name: str = ""):
    timestamp = int(time.time())
    with open(f"{file_name}_test_cases_{timestamp}.json", "w") as f:
        f.write(test_cases)