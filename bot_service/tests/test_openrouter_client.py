import pytest
import respx
import httpx
from httpx import Response
from app.services.openrouter_client import OpenRouterClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_openrouter_client_success():
    client = OpenRouterClient()
    
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Привет!"
                }
            }
        ]
    }
    
    with respx.mock(base_url=settings.OPENROUTER_BASE_URL) as respx_mock:
        respx_mock.post("/chat/completions").mock(
            return_value=Response(200, json=mock_response)
        )
        
        result = await client.get_completion("Скажи привет")
        
        assert result == "Привет!"

@pytest.mark.asyncio
async def test_openrouter_client_http_error():
    client = OpenRouterClient()
    
    with respx.mock(base_url=settings.OPENROUTER_BASE_URL) as respx_mock:
        respx_mock.post("/chat/completions").mock(
            return_value=Response(500, text="Internal Server Error")
        )
        
        result = await client.get_completion("Тест")
        
        assert "Ошибка OpenRouter: статус 500" in result

@pytest.mark.asyncio
async def test_openrouter_client_timeout():
    client = OpenRouterClient()
    
    with respx.mock(base_url=settings.OPENROUTER_BASE_URL) as respx_mock:
        respx_mock.post("/chat/completions").mock(side_effect=httpx.TimeoutException("Timeout"))
        
        result = await client.get_completion("Тест")
        
        assert "превышено время" in result or "Timeout" in result
