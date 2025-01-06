from prefect import task
from openai import OpenAI
from src.config import (AZURE_MISTRAL_SMALL_API, AZURE_MISTRAL_SMALL_INFERENCE_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
                    OPENROUTER_MODEL_MISTRAL_FREE, 
                    AZURE_MISTRAL_LARGE_API, AZURE_MISTRAL_LARGE_INFERENCE_KEY,
                    AZURE_OPENAI_API_BASE, AZURE_OPENAI_API_KEY_GPT_4o,
                    AZURE_OPENAI_API_VERSION, AZURE_OPENAI_API_KEY_GPT_4o_MINI,
                    AZURE_OPENAI_API_GPT_4o_MINI, AZURE_OPENAI_API_GPT_4o)
import requests
from .image import encode_image
class LLMClient:
    def __init__(self, 
                 use_azure_mistral: bool = False,
                 use_azure_openai: bool = False,
                 use_openrouter: bool = False,
                 use_anthropic: bool = False,
                 use_openai: bool = False,
                 model: str = "",
                 app: str = "newsletterdigest"):
        self.use_azure_mistral = use_azure_mistral
        self.use_azure_openai = use_azure_openai
        self.use_openrouter = use_openrouter
        self.use_anthropic = use_anthropic
        self.use_openai = use_openai
        self.model = model
        self.app = app
        print(f"LLMClient init: use_azure_mistral: {self.use_azure_mistral}, use_azure_openai: {self.use_azure_openai}, use_openrouter: {self.use_openrouter}, use_anthropic: {self.use_anthropic}, use_openai: {self.use_openai}, model: {self.model}, app: {self.app}")

    @task(log_prints=True, cache_policy=None, retries=2)
    def call_llm(self, 
                sys_prompt: str, 
                user_input: str,
                image_path: str = "",
                ai_input: str = ""):
        try:
            response = ""
            if self.use_azure_mistral:
                if self.model.lower() == "small":
                    response = self._call_azure_mistral(sys_prompt, user_input, ai_input, AZURE_MISTRAL_SMALL_API, AZURE_MISTRAL_SMALL_INFERENCE_KEY)
                elif self.model.lower() == "large":
                    response = self._call_azure_mistral(sys_prompt, user_input, ai_input, AZURE_MISTRAL_LARGE_API, AZURE_MISTRAL_LARGE_INFERENCE_KEY)
            elif self.use_azure_openai:
                response = self._call_azure_openai(sys_prompt, user_input, image_path)
            elif self.use_openrouter:
                if self.model == "":
                    self.model = OPENROUTER_MODEL_MISTRAL_FREE
                response = self._call_openrouter(sys_prompt, user_input, ai_input)
            elif self.use_anthropic:
                response = self._call_anthropic(sys_prompt, user_input, ai_input)
            elif self.use_openai:
                response = self._call_openai(sys_prompt, user_input, ai_input)
            else:
                raise ValueError("No LLM provider selected")
            if response is None:
                return "LLM response is None"
            return response
        except Exception as e:
            print(f"LLM Call Warning: {e}")
            return f"LLM Call Warning: {e}"

    def _call_openrouter(self, sys_prompt: str, user_input: str, ai_input: str) -> str:
        print(f"Calling OpenRouter with {self.model} ...")
        llm = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )
        response = llm.chat.completions.create(
            extra_headers={"HTTP-Referer": f"https://{self.app}.com", "X-Title": self.app},
            model=self.model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "assistant", "content": ai_input},
                {"role": "user", "content": user_input},
            ],
            max_tokens=10000,
        )
        return response.choices[0].message.content

    def _call_openai(self, sys_prompt: str, user_input: str, ai_input: str) -> str:
        llm = OpenAI(api_key=OPENAI_API_KEY)
        response = llm.chat.completions.create(
            model=self.model,
            temperature=0.7,
            messages=[
                {"role": "user", "content": sys_prompt},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": ai_input}
            ],
        )
        return response.choices[0].message.content

    def _call_anthropic(self, sys_prompt: str, user_input: str, ai_input: str) -> str:
        from anthropic import Anthropic
        llm = Anthropic(api_key=ANTHROPIC_API_KEY)
        response = llm.messages.create(
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"{sys_prompt}, the user input:\n {user_input}",
            }],
            model=self.model
        )
        return response.content[0].text

    def _call_azure_mistral(self, sys_prompt: str, user_input: str, ai_input: str, endpoint: str, inference_key: str) -> str:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential
        print(f"Calling Azure Mistral with {self.model} model ...")
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(inference_key)
        )
        messages = [{"role": "user", "content": f"<s>[INST]<<SYS>>{ sys_prompt }<</SYS>>"}]
        if ai_input:
            messages.append({"role": "assistant", "content": ai_input})
        messages.append({"role": "user", "content": user_input})
        
        payload = {
            "messages": messages,
            "max_tokens": 8192,
            "temperature": 0.7,
            "top_p": 0.7
        }
        response = client.complete(payload)
        return response.choices[0].message.content

    def _call_azure_openai(self, sys_prompt: str, question: str, image_path: str = "") -> str:
        if self.model == AZURE_OPENAI_API_GPT_4o_MINI or self.model == "":
            model = AZURE_OPENAI_API_GPT_4o_MINI
            api_key = AZURE_OPENAI_API_KEY_GPT_4o_MINI
        else:
            model = AZURE_OPENAI_API_GPT_4o
            api_key = AZURE_OPENAI_API_KEY_GPT_4o
        print(f"Calling Azure OpenAI with {model}, image_path: {image_path} ...")
        # Configuration
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }
        # Payload for the request
        user_input = {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
        if image_path != "":
            base64_image = encode_image(image_path)
            if base64_image:  # Check if base64_image is not empty
                user_input["content"].append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_image
                        }
                    }
                )
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": sys_prompt
                        }
                    ]
                },
                user_input
            ],
            "temperature": 0.7,
            "top_p": 0.7,
            "max_tokens": 8192
        }
        url = f"{AZURE_OPENAI_API_BASE}/openai/deployments/{model}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
        # Send request
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
        response_json = response.json()
        print(response_json)
        return response_json["choices"][0]["message"]["content"]