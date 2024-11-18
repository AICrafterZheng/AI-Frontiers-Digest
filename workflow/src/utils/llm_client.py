from prefect import task
from openai import OpenAI
from src.config import (AZURE_MISTRAL_SMALL_API, AZURE_MISTRAL_SMALL_INFERENCE_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY,
                    OPENROUTER_MODEL_MISTRAL_FREE, OPENAI_MODEL, ANTHROPIC_MODEL)

class LLMClient:
    def __init__(self, 
                 use_azure: bool = False,
                 use_openrouter: bool = False,
                 use_anthropic: bool = False,
                 use_openai: bool = False,
                 model: str = "",
                 app: str = "newsletterdigest"):
        self.use_azure = use_azure
        self.use_openrouter = use_openrouter
        self.use_anthropic = use_anthropic
        self.use_openai = use_openai
        self.model = model
        self.app = app
        print(f"LLMClient init: use_azure: {self.use_azure}, use_openrouter: {self.use_openrouter}, use_anthropic: {self.use_anthropic}, use_openai: {self.use_openai}, model: {self.model}, app: {self.app}")

    @task(log_prints=True)
    def call_llm(self, 
                sys_prompt: str, 
                user_input: str, 
                ai_input: str = ""):
        try:
            response = ""
            if self.use_azure:
                response = self._call_azure(sys_prompt, user_input, ai_input)
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
            print(f"LLM Call Error: {e}")
            return f"LLM Call Error: {e}"

    def _call_openrouter(self, sys_prompt: str, user_input: str, ai_input: str) -> str:
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

    def _call_azure(self, sys_prompt: str, user_input: str, ai_input: str) -> str:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential
        
        client = ChatCompletionsClient(
            endpoint=AZURE_MISTRAL_SMALL_API,
            credential=AzureKeyCredential(AZURE_MISTRAL_SMALL_INFERENCE_KEY)
        )
        messages = [{"role": "user", "content": f"<s>[INST]<<SYS>>{ sys_prompt }<</SYS>>"}]
        if ai_input:
            messages.append({"role": "assistant", "content": ai_input})
        messages.append({"role": "user", "content": user_input})
        
        payload = {
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.1
        }
        response = client.complete(payload)
        return response.choices[0].message.content

# Example usage:
if __name__ == "__main__":
    llm_client = LLMClient(use_azure=True)
    response = llm_client.call_llm("tell me a joke", "You are a helpful assistant")
    print(response)