import aiohttp
import logging
from typing import List, Dict, Any

class BybitP2PClient:
    URL = "https://api2.bybit.com/fiat/otc/item/online"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def fetch_orders(self, side: str, fiat: str = "RUB", payment_code: str = "75") -> List[Dict[str, Any]]:
        """
        side: '1' - Покупка USDT (Maker продает), '0' - Продажа USDT (Maker покупает)
        payment_code: '75' - Т-Банк, '582' - Сбер, '382' - Райффайзен
        """
        payload = {
            "userId": "",
            "tokenId": "USDT",
            "currencyId": fiat,
            "payment": [payment_code] if payment_code else [],
            "side": side,
            "size": "10",
            "page": "1",
            "amount": "",
            "authMaker": False,
            "canTrade": False
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.post(self.URL, json=payload, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("result", {}).get("items", [])
                        return self._filter_merchants(items)
                    logging.error(f"Bybit API Error Status: {response.status}")
            except Exception as e:
                logging.error(f"Сбой при запросе P2P стакана Bybit: {e}")
        return []

    def _filter_merchants(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Фильтрация неблагонадежных мерчантов по проценту сделок и объему"""
        filtered = []
        for item in items:
            finish_rate = float(item.get("recentExecuteRate", 0))
            recent_orders = int(item.get("recentOrderNum", 0))

            # Фильтр качества: от 90% завершенных ордеров и от 30+ сделок
            if finish_rate >= 90 and recent_orders >= 30:
                filtered.append({
                    "id": item.get("id"),
                    "nickName": item.get("nickName"),
                    "price": float(item.get("price")),
                    "minAmount": float(item.get("minAmount", 0)),
                    "maxAmount": float(item.get("maxAmount", 0)),
                    "finishRate": finish_rate,
                    "recentOrders": recent_orders
                })
        return filtered
