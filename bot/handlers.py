from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "🚀 **Crypto P2P Arbitrage Scanner Bot запущен!**\n\n"
        "Сигналы об аномальных спредах автоматически публикуются в ваш целевой канал.\n"
        "Убедитесь, что бот добавлен администратором в канал."
    )
