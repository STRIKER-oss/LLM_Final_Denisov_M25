import httpx
from app.core.config import settings

class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
    
    async def get_completion(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"Ошибка OpenRouter: статус {response.status_code}"
            
            except httpx.TimeoutException:
                return "Ошибка: превышено время ожидания ответа от LLM"
            except httpx.RequestError as e:
                return f"Ошибка сети: {str(e)}"
            except Exception as e:
                return f"Ошибка: {str(e)}"
