from aiogram import Router, types
from aiogram.filters import Command
from app.infra.redis import get_redis
from app.core.jwt import decode_and_validate
from app.tasks.llm_tasks import llm_request
import asyncio

router = Router()

def register_handlers(dp):
    dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать!\n"
        "Используйте /token <ваш_jwt_токен> для авторизации\n"
        "После авторизации отправляйте текст для получения ответа от LLM"
    )

@router.message(Command("token"))
async def cmd_token(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Использование: /token <jwt_токен>")
        return
    
    jwt_token = args[1]
    
    try:
        payload = decode_and_validate(jwt_token)
        user_id = payload.get("sub")
        if not user_id:
            await message.answer("Неверный формат токена: отсутствует sub")
            return
        
        redis = await get_redis()
        await redis.setex(f"user_token:{message.from_user.id}", 3600, jwt_token)
        await message.answer(f"Токен сохранён. Вы авторизованы как пользователь {user_id}")
    
    except ValueError as e:
        await message.answer(f"Ошибка валидации токена: {str(e)}")

@router.message()
async def handle_text(message: types.Message):
    redis = await get_redis()
    token_key = f"user_token:{message.from_user.id}"
    jwt_token = await redis.get(token_key)
    
    if not jwt_token:
        await message.answer(
            "Вы не авторизованы. Используйте /token <jwt_токен> для авторизации.\n"
            "Получите токен в Auth Service через POST /auth/login"
        )
        return
    
    try:
        payload = decode_and_validate(jwt_token)
        user_id = payload.get("sub")
        
        llm_request.delay(message.from_user.id, message.text)
        
        await message.answer(
            f"Запрос принят (пользователь {user_id}). "
            "Обработка может занять некоторое время. "
            "Результат придёт отдельным сообщением."
        )
        
        await asyncio.sleep(2)
        result_key = f"llm_result:{message.from_user.id}"
        result = await redis.get(result_key)
        
        if result:
            await message.answer(f"Ответ LLM:\n\n{result[:4000]}")
            await redis.delete(result_key)
        else:
            await message.answer("Ответ ещё не готов. Пожалуйста, подождите.")
    
    except ValueError as e:
        await message.answer(f"Ошибка авторизации: {str(e)}. Пожалуйста, получите новый токен.")
