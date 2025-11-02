import aiohttp
import asyncio
import requests

API_URL_TEMPLATE = "https://api.mcsrvstat.us/3/{}"
# 가독성, 재사용성을 위해 상수로 선언

def get_player_count(ip: str) -> dict[str, int]:
    response = requests.get(API_URL_TEMPLATE.format(ip), timeout=10)
    if response.status_code == 200:
        data = response.json()
        if data["online"]:
            return data["players"]
    return {"online": 0, "max": 0} # 기본값 플레이어 0명

if __name__ == "__main__":
    # 테스트용 메인 블록
    test_ip = "pixel.mc-complex.com"
    # player_count = asyncio.run(get_server_player_count(test_ip))
    player_count = get_player_count(test_ip)
    print(f"Server {test_ip} has {player_count} online players.")