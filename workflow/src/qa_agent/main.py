from src.utils.llm_client import LLMClient
from .prompts import SYS_PROMPT_JSON, SS_TO_DESCRIPTION, SYS_PROMPT_JSON_V2
from src.utils.helpers import extract_llm_response
from src.config import AZURE_OPENAI_API_GPT_4o

def gen_test_cases(web_desc: str):
    llm_client = LLMClient(use_azure_openai=True, model=AZURE_OPENAI_API_GPT_4o)
    sys_promt = SYS_PROMPT_JSON_V2.format(description=web_desc)
    response = llm_client.call_llm(sys_promt, "Create test cases for the webpage")
    md = extract_llm_response(response, "test_cases")
    # write to markdown file
    timestamp = int(time.time())
    with open(f"test_cases_{timestamp}.json", "w") as f:
        f.write(md)
    print("response \n", response)

def gen_test_cases_with_image(image_paths: list[str]):
    llm_client = LLMClient(use_azure_openai=True, model=AZURE_OPENAI_API_GPT_4o)
    response = llm_client.call_llm(SYS_PROMPT_JSON, "Create test cases for the webpage", image_paths)
    md = extract_llm_response(response, "test_cases")
    # write to markdown file
    timestamp = int(time.time())
    with open(f"test_cases_{timestamp}.json", "w") as f:
        f.write(md)
    print("response \n", response)

def screenshot_to_description(image_path: str):
    llm_client = LLMClient(use_azure_openai=True, model=AZURE_OPENAI_API_GPT_4o)
    response = llm_client.call_llm(SS_TO_DESCRIPTION, "Describe the screenshot", [image_path])
    return extract_llm_response(response, "webpage_description")

