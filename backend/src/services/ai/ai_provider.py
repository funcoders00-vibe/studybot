import os
import logging
from openai import OpenAI
from src.settings import settings

logger = logging.getLogger(__name__)

class AIProvider:
    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 4096, temperature: float = 0.2) -> str:
        raise NotImplementedError

class NVIDIAProvider(AIProvider):
    def __init__(self, api_key: str | None = None, model: str = 'nvidia/nemotron-3.5-lightning-30b-a3b'):
        self.api_key = api_key or settings.nvidia_api_key
        self.model = model
        self.base_url = 'https://integrate.api.nvidia.com/v1'

    def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 4096, temperature: float = 0.2) -> str:
        if not self.api_key:
            raise RuntimeError("NVIDIA_API_KEY is not configured.")
        client = OpenAI(base_url=self.base_url, api_key=self.api_key, timeout=3.0, max_retries=0)
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95
        )
        content = response.choices[0].message.content or ''
        return content.strip()

def get_ai_provider() -> AIProvider:
    return NVIDIAProvider()
