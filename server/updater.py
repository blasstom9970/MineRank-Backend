# 서버 업데이트 관련 함수 모음 (서버 랭크 갱신, 서버 플레이어 수 갱신, 서버 추가)

from datetime import datetime, timezone
import server.api_request as api
from duckdb import DuckDBPyConnection
from concurrent.futures import ThreadPoolExecutor, as_completed

def update_player_counts(cursor: DuckDBPyConnection, server_list: list[dict]):
    """마지막 업데이트로부터 오래된 서버들만 병렬로 갱신하고 DB 업데이트는 순차로 수행합니다."""
    to_update = []
    for server in server_list:
        last_updated = datetime.fromisoformat(server['updated_at'].replace('Z', '+00:00'))
        elapsed = (datetime.now(timezone.utc) - last_updated).total_seconds()
        if elapsed >= 3600:
            to_update.append(server['ip'])

    if not to_update:
        return

    # 병렬로 API 호출(블로킹을 메인 쓰레드에서 분리)
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(api.get_player_count, ip): ip for ip in to_update}
        for fut in as_completed(futures):
            ip = futures[fut]
            try:
                pl = fut.result()
            except Exception as e:
                print(f"Failed fetching {ip}: {e}")
                pl = {"online": 0, "max": 0}
            cursor.execute(
                "UPDATE servers SET online = ?, maxPlayers = ?, updated_at = ? WHERE ip = ?;",
                (pl['online'], pl['max'], datetime.now(timezone.utc).isoformat() + 'Z', ip)
            )

def add_new_server(server_data: dict) -> dict:
    """새로운 서버를 데이터베이스에 추가합니다."""
    pl = api.get_player_count(server_data['ip'])
    server_data['online'] = pl['online']
    server_data['maxPlayers'] = pl['max']
    server_data['updated_at'] = datetime.now(timezone.utc).isoformat() + 'Z'
    server_data['rank'] = 1  # 랭크는 나중에 배정

    return server_data

def update_servers_rank(cursor: DuckDBPyConnection):
    """서버 랭크를 플레이어 수 기준으로 갱신합니다."""
    server_list = cursor.execute("SELECT ip, online FROM servers ORDER BY online DESC;").fetchall()
    for rank, (ip, _) in enumerate(server_list, start=1):
        cursor.execute(
            "UPDATE servers SET rank = ? WHERE ip = ?;",
            (rank, ip)
        )