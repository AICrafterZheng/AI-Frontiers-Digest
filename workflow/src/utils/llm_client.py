from prefect import task
from openai import OpenAI
from src.config import(AZURE_OPENAI_API_VERSION)
import requests
from .image import encode_image
from src.common import LLMProvider, LLM_2_ENDPOINT, LLM_2_INFERENCE_KEY, LLM_2_MODEL

class LLMClient:
    def __init__(self, llm_provider: LLMProvider = LLMProvider.AZURE_OPENAI_GPT_4o):
        self.model = LLM_2_MODEL.get(llm_provider)
        self.llm_endpoint = LLM_2_ENDPOINT.get(llm_provider)
        self.llm_inference_key = LLM_2_INFERENCE_KEY.get(llm_provider)
        self.llm_provider = llm_provider
        print(f"LLMClient init: llm_provider: {self.llm_provider}, model: {self.model}, endpoint: {self.llm_endpoint}")

    @task(log_prints=True, cache_policy=None, retries=2)
    def call_llm(self, 
                sys_prompt: str, 
                user_input: str,
                image_paths: list = None,
                ai_input: str = ""):
        try:
            response = ""
            if self.llm_provider == LLMProvider.AZURE_MISTRAL_SMALL or self.llm_provider == LLMProvider.AZURE_MISTRAL_LARGE or self.llm_provider == LLMProvider.AZURE_DEEPSEEK:
                    response = self._call_azure_llm(sys_prompt, user_input, ai_input)
            elif self.llm_provider == LLMProvider.AZURE_OPENAI_GPT_4o or self.llm_provider == LLMProvider.AZURE_OPENAI_GPT_4o_MINI:
                response = self._call_azure_openai(sys_prompt, user_input, image_paths)
            elif self.llm_provider == LLMProvider.OPENROUTER:
                response = self._call_openrouter(sys_prompt, user_input, ai_input)
            elif self.llm_provider == LLMProvider.ANTHROPIC:
                response = self._call_anthropic(sys_prompt, user_input)
            elif self.llm_provider == LLMProvider.OPENAI:
                response = self._call_openai(sys_prompt, user_input, ai_input)
            else:
                raise ValueError("No LLM provider selected")
            if response is None:
                return "LLM response is None"
            return response
        except Exception as e:
            print(f"LLM Call error: {e}")
            return f"LLM Call error: {e}"

    def _call_openrouter(self, sys_prompt: str, user_input: str, ai_input: str) -> str:
        print(f"Calling OpenRouter with {self.model} ...")
        app_name = "newsletterdigest"
        llm = OpenAI(
            base_url=self.llm_endpoint,
            api_key=self.llm_inference_key
        )
        response = llm.chat.completions.create(
            extra_headers={"HTTP-Referer": f"https://{app_name}.com", "X-Title": app_name},
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
        llm = OpenAI(api_key=self.llm_inference_key)
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

    def _call_anthropic(self, sys_prompt: str, user_input: str) -> str:
        from anthropic import Anthropic
        llm = Anthropic(api_key=self.llm_inference_key)
        response = llm.messages.create(
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"{sys_prompt}, the user input:\n {user_input}",
            }],
            model=self.model
        )
        return response.content[0].text

    def _call_azure_llm(self, sys_prompt: str, user_input: str, ai_input: str) -> str:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential
        print(f"Calling Azure LLM with {self.llm_provider}...")
        client = ChatCompletionsClient(
            endpoint=self.llm_endpoint,
            credential=AzureKeyCredential(self.llm_inference_key)
        )
        model_info = client.get_model_info()
        print("Model name:", model_info.model_name)
        print("Model type:", model_info.model_type)
        print("Model provider name:", model_info.model_provider_name)

        messages = [{"role": "user", "content": f"<s>[INST]<<SYS>>{ sys_prompt }<</SYS>>"}]
        if ai_input:
            messages.append({"role": "assistant", "content": ai_input})
        messages.append({"role": "user", "content": user_input})
        
        payload = {
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.7
        }
        response = client.complete(payload)
        return response.choices[0].message.content

    def _call_azure_openai(self, sys_prompt: str, question: str, image_paths: list = None) -> str:
        print(f"Calling Azure OpenAI with {self.model}, image_paths: {image_paths} ...")
        # Configuration
        headers = {
            "Content-Type": "application/json",
            "api-key": self.llm_inference_key,
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
        if image_paths != None:
            for image_path in image_paths:
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
        url = f"{self.llm_endpoint}/openai/deployments/{self.model}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
        # Send request
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
        response_json = response.json()
        print(response_json)
        return response_json["choices"][0]["message"]["content"]