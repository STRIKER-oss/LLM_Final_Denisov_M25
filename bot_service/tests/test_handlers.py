import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, User, Chat
from app.bot.handlers import cmd_start, cmd_token, handle_text

@pytest.fixture
def fake_message():
    msg = AsyncMock(spec=Message)
    msg.from_user = User(id=123456, is_bot=False, first_name="Test")
    msg.chat = Chat(id=123456, type="private")
    msg.text = ""
    msg.answer = AsyncMock()
    return msg

@pytest.fixture
async def mock_redis():
    import fakeredis.aioredis
    from unittest.mock import patch
    
    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    
    async def mock_get_redis():
        return fake_redis
    
    with patch("app.bot.handlers.get_redis", mock_get_redis):
        with patch("app.tasks.llm_tasks.get_redis", mock_get_redis):
            yield fake_redis
    
    await fake_redis.close()

@pytest.mark.asyncio
async def test_cmd_start(fake_message):
    fake_message.text = "/start"
    await cmd_start(fake_message)
    fake_message.answer.assert_called_once()
    assert "Добро пожаловать" in fake_message.answer.call_args[0][0]

@pytest.mark.asyncio
async def test_cmd_token_saves_to_redis(fake_message, mock_redis):
    fake_message.text = "/token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
    
    with patch("app.bot.handlers.decode_and_validate") as mock_decode:
        mock_decode.return_value = {"sub": "42"}
        await cmd_token(fake_message)
    
    saved_token = await mock_redis.get("user_token:123456")
    assert saved_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
    fake_message.answer.assert_called_with("Токен сохранён. Вы авторизованы как пользователь 42")

@pytest.mark.asyncio
async def test_cmd_token_invalid_format(fake_message):
    fake_message.text = "/token"
    await cmd_token(fake_message)
    fake_message.answer.assert_called_with("Использование: /token <jwt_токен>")

@pytest.mark.asyncio
async def test_cmd_token_invalid_jwt(fake_message):
    fake_message.text = "/token invalid.token"
    
    with patch("app.bot.handlers.decode_and_validate") as mock_decode:
        mock_decode.side_effect = ValueError("Invalid token")
        await cmd_token(fake_message)
    
    fake_message.answer.assert_called_with("Ошибка валидации токена: Invalid token")

@pytest.mark.asyncio
async def test_handle_text_no_token(fake_message, mock_redis):
    fake_message.text = "Привет, как дела?"
    await handle_text(fake_message)
    fake_message.answer.assert_called_with(
        "Вы не авторизованы. Используйте /token <jwt_токен> для авторизации.\n"
        "Получите токен в Auth Service через POST /auth/login"
    )

@pytest.mark.asyncio
async def test_handle_text_with_valid_token(fake_message, mock_redis):
    await mock_redis.setex("user_token:123456", 3600, "valid.jwt.token")
    fake_message.text = "Напиши стих"
    
    with patch("app.bot.handlers.decode_and_validate") as mock_decode:
        mock_decode.return_value = {"sub": "42"}
        with patch("app.bot.handlers.llm_request.delay") as mock_delay:
            await handle_text(fake_message)
    
    mock_delay.assert_called_once_with(123456, "Напиши стих")
    fake_message.answer.assert_any_call(
        "Запрос принят (пользователь 42). "
        "Обработка может занять некоторое время. "
        "Результат придёт отдельным сообщением."
    )
