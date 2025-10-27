import requests
import json

def get_server_player_count(ip):
    try:
        response = requests.get(f"https://api.mcsrvstat.us/3/{ip}")
        if response.status_code == 200:
            data = response.json()
            if (data["online"]):
                return data["players"]["online"]
            else:
                return 0 # 서버가 오프라인인 경우 플레이어 0명

    except Exception as e:
        print(f"Error fetching server data: {e}")
        return None