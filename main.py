import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from bot import router, send_p2p_signal
from services import BybitP2PClient
from database import redis_cache

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def p2p_scanner_loop(bot: Bot):
    client = BybitP2PClient()
    banks = [
        ("75", "Т-Банк"), 
        ("582", "Сбер"), 
        ("382", "Райффайзен")
    ]
    
    logging.info("🚀 P2P Сканер запущен в фоновом режиме...")

    while True:
        for bank_code, bank_name in banks:
            try:
                buy_orders = await client.fetch_orders(side="1", payment_code=bank_code)
                sell_orders = await client.fetch_orders(side="0", payment_code=bank_code)

                if buy_orders and sell_orders:
                    best_buy = buy_orders[0]
                    best_sell = sell_orders[0]

                    spread = ((best_sell["price"] - best_buy["price"]) / best_buy["price"]) * 100

                    if spread >= settings.MIN_SPREAD_PERCENT:
                        signal_key = f"bybit:{bank_code}:{best_buy['price']}:{best_sell['price']}"
                        
                        if not await redis_cache.is_signal_duplicate(signal_key, ttl=180):
                            msg = (
                                f"🔥 **ОБНАРУЖЕН СПРЕД НА {bank_name.upper()}: {spread:.2f}%**\n\n"
                                f"💵 **Покупка USDT:** `{best_buy['price']} RUB` ({best_buy['nickName']})\n"
                                f"💳 **Продажа USDT:** `{best_sell['price']} RUB` ({best_sell['nickName']})\n"
                                f"📊 **Исполнение:** {best_buy['finishRate']}% / {best_sell['finishRate']}%\n"
                                f"💰 **Профит с 100k ₽:** ~{((100000 / best_buy['price']) * best_sell['price']) - 100000:.0f} ₽"
                            )
                            await send_p2p_signal(bot, msg)
            except Exception as e:
                logging.error(f"Ошибка в цикле сканера для банка {bank_name}: {e}")

        await asyncio.sleep(settings.SCAN_INTERVAL_SECONDS)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Запуск фоновой таски сканирования
    asyncio.create_task(p2p_scanner_loop(bot))

    logging.info("🤖 Запуск Telegram бота...")
    try:
        await dp.start_polling(bot)
    finally:
        await redis_cache.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
