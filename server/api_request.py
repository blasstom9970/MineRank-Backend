import aiohttp
import asyncio
import json

async def fetch(session:aiohttp.ClientSession, url):
    timeout = aiohttp.ClientTimeout(total=10)

    async with session.get(url, timeout=timeout) as response:
        return response

async def get_server_player_count(ip):
    async with aiohttp.ClientSession() as session:
        try:
            response = await fetch(session, f"https://api.mcsrvstat.us/3/{ip}")
            if response.status == 200:
                data = await response.json()
                if (data["online"]):
                    return data["players"]["online"]
                else:
                    return 0 # 서버가 오프라인인 경우 플레이어 0명
            else:
                return 0 # 응답 코드가 200이 아닌 경우 플레이어 0명 

        except Exception as e:
            print(f"Error fetching server data: {e}")
            return 0