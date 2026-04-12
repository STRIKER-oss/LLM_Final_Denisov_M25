from celery import shared_task
import httpx
from app.core.config import settings
import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

@shared_task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_process_llm_request(tg_chat_id, prompt))
    loop.close()

async def _process_llm_request(tg_chat_id: int, prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
        else:
            answer = f"Ошибка LLM: {response.status_code}"
        
        bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await bot.send_message(chat_id=tg_chat_id, text=f"Ответ LLM:\n\n{answer[:4000]}")
        await bot.session.close()
