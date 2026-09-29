# ⚡ Crypto P2P Arbitrage & Spread Scanner Bot

Высокоскоростной асинхронный сканер арбитражных связок и спредов P2P-рынка (Bybit / RUB) с фильтрацией мерчантов и защитой от спама через Redis.

## ⚡ Особенности
- 🚀 **Низкая задержка (Low Latency)** — асинхронный опрос стаканов ордеров через `aiohttp`.
- 🏦 **Поддержка популярных банков** — Т-Банк, Сбербанк, Райффайзен.
- 🛡 **Защита от флуда и спама** — асинхронный кеш Redis блокирует повторяющиеся сигналы на заданный TTL.
- 🔍 **Умная фильтрация** — отсеивание неопытных продавцов (учитывается % завершенных сделок и их количество).
- 📱 **Telegram-уведомления** — мгновенная публикация выгодных спредов в приватный канал с расчетом чистого профита.

## 🛠️ Стек технологий
- **Python 3.10+**
- **aiogram 3.x** (Telegram Bot API)
- **aiohttp** (Async HTTP Client)
- **redis-py** (Async Redis Driver)
- **Pydantic Settings** (Валидация конфигурации)

## 📁 Структура проекта
```text
crypto-p2p-arbitrage-scanner/
├── bot/
│   ├── __init__.py
│   ├── handlers.py        # Обработчики команд бота
│   └── notifier.py        # Отправка алертов в канал
├── database/
│   ├── __init__.py
│   └── redis_db.py        # Кеш-память Redis (дедупликация)
├── services/
│   ├── __init__.py
│   └── bybit_p2p.py       # API Клиент Bybit P2P
├── config.py              # Конфигурация
├── main.py                # Точка входа
├── requirements.txt
└── README.md
```

## 🚀 Быстрый запуск

1. Клонировать репозиторий:
```bash
git clone [https://github.com/fallenworked/crypto-p2p-arbitrage-scanner.git](https://github.com/fallenworked/crypto-p2p-arbitrage-scanner.git)
cd crypto-p2p-arbitrage-scanner
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Указать `BOT_TOKEN` и `CHANNEL_ID` в `config.py`.

4. Убедиться, что сервис Redis запущен (`redis-server`).

5. Запустить скрипт:
```bash
python main.py
```

## 👨‍💻 Автор и контакты
- **Автор**: fallenworked
- **GitHub**: [fallenworked](https://github.com/fallenworked)
- **Telegram**: [@caxaold](https://t.me/caxaold)
