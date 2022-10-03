import aiohttp
from config import ETHERSCAN_TOKEN


async def etherscan_status() -> bool:
    URL = f'http://api.etherscan.io/api?module=account&action=txlist&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={ETHERSCAN_TOKEN}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            # интеграция не прошла если сервер не отдает запрос
            if response.status != 200:
                return False

            try:
                # парсим json ответ
                json_response = await response.json()
                integration_result = int(json_response['status'])
            except:
                return False

            # проверяем статус
            if integration_result == 1:
                return True
            return False
