import aiohttp
import asyncio

API_URL_TEMPLATE = "https://api.mcsrvstat.us/3/{}"
# 가독성, 재사용성을 위해 상수로 선언

async def fetch(session, url, timeout = 10): 
    if type(timeout) in [int, float]: # 가독성을 위해 조건부 쉽게 변경
        timeout = aiohttp.ClientTimeout(total = timeout)
    async with session.get(url, timeout = timeout) as response:
        return response

async def get_server_player_count(ip: str) -> int:
    async with aiohttp.ClientSession() as session:
        try:
            url = API_URL_TEMPLATE.format(ip)
            response = await fetch(session, url)
            if response.status == 200:
                data = await response.json()
                if data["online"]:
                    return data["players"]["online"]
                else:
                    return 0 # 서버가 오프라인인 경우 플레이어 0명
            else:
                return 0 # 응답 코드가 200이 아닌 경우 플레이어 0명 

        except Exception as e:
            print(f"Error fetching server data: {e}")
            return 0