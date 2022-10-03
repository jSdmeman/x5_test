import aiohttp


async def selectel_status() -> bool:
    URL = f'http://selectel.status.io/1.0/status/5980813dd537a2a7050004bd'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            # интеграция не прошла если сервер не отдает запрос
            if response.status != 200:
                return False
            
            try:
                # парсим json ответ
                json_response = await response.json()
                integration_result = int(json_response['result']['status_overall']['status_code'])
            except:
                return False

            # проверяем статус
            if integration_result == 100:
                return True
            return False
