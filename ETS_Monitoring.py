import aiohttp
import asyncio

# Steam API Configuration
STEAM_API_KEY = 'ключ steam api'
ip = 'IP сервера'
port = 'Query порт сервера'
SERVER_APP_ID = '227300' #id игры в стиме
PLAYER_CHECK_INTERVAL_SEC = 5

async def fetch_steam_data(ip, port, app_id):
    url = f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={STEAM_API_KEY}&filter=addr%5C{ip}:{port}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

async def send_discord_message(webhook_url, message, embed=None):
    async with aiohttp.ClientSession() as session:
        webhook_data = {
            "content": message,
            "username": "Server Monitor",
            # "avatar_url": "URL к иконке бота (если необходимо)"
        }
        # Проверяем, был ли добавлен embed
        if embed:
            webhook_data["embeds"] = [embed]  # Discord принимает массив эмбедов

        await session.post(webhook_url, json=webhook_data)

async def player_count_monitor(webhook_url):  # Добавляем параметр для URL вебхука
    prev_player_count = None  # Изменяем значение по умолчанию
    while True:
        steam_data = await fetch_steam_data(ip, port, SERVER_APP_ID)
        if steam_data and steam_data.get("response") and steam_data["response"].get("servers"):
            current_player_count = steam_data["response"]["servers"][0].get("players", 0)

            # Создание эмбеда
            embed = {
                "title": "Изменение количества игроков на сервере",
                "description": f"Текущее количество игроков на сервере: {current_player_count}",
                "color": 5814783,  # Выберите цвет как нравится
                "fields": [
                    {
                        "name": "IP сервера",
                        "value": ip,
                        "inline": True
                    },
                    {
                        "name": "Порт сервера",
                        "value": port,
                        "inline": True
                    },
                ]
            }

            if prev_player_count is not None and prev_player_count < current_player_count:
                message = f"Новый игрок теперь в конвое ETS."
                await send_discord_message(webhook_url, message, embed)
            elif prev_player_count is not None and prev_player_count > current_player_count:
                message = f"Кто-то покинул конвой ETS."
                await send_discord_message(webhook_url, message, embed)

            prev_player_count = current_player_count

     #   else:
  #          await send_discord_message(webhook_url, "Не удалось получить данные о сервере.", embed)

        await asyncio.sleep(PLAYER_CHECK_INTERVAL_SEC)

asyncio.run(player_count_monitor('https://discord.com/api/webhooks/... ВАШ ДИСКОРД ВЕБХУК'))

