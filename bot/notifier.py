import logging
from aiogram import Bot
from config import settings

async def send_p2p_signal(bot: Bot, signal_msg: str):
    """Публикация найденного спреда в Telegram-канал"""
    try:
        await bot.send_message(
            chat_id=settings.CHANNEL_ID,
            text=signal_msg,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(f"❌ Не удалось отправить сигнал в Telegram: {e}")
