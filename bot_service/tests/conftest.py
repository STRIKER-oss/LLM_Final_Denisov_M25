import pytest
import fakeredis.aioredis
from unittest.mock import patch

@pytest.fixture
async def mock_redis():
    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    
    async def mock_get_redis():
        return fake_redis
    
    with patch("app.bot.handlers.get_redis", mock_get_redis):
        with patch("app.tasks.llm_tasks.get_redis", mock_get_redis):
            yield fake_redis
    
    await fake_redis.close()

@pytest.fixture
def anyio_backend():
    return "asyncio"
