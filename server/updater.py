# 서버 업데이트 관련 함수 모음 (서버 랭크 갱신, 서버 플레이어 수 갱신, 서버 추가)

from datetime import datetime, timezone
import server.api_request as api
from duckdb import DuckDBPyConnection

def update_player_counts(cursor: DuckDBPyConnection, server_list: list[dict]):
    """마지막 업데이트로 부터 일정 시간이 지난 서버들의 플레이어 수를 갱신합니다."""
    for server in server_list:
        last_updated = datetime.fromisoformat(server['updated_at'].replace('Z', '+00:00'))
        elapsed = (datetime.now(timezone.utc) - last_updated).total_seconds()

        if elapsed >= 3600:  # 1시간 이후에 업데이트된 서버만 업데이트
            ip = server['ip']
            pl = api.get_player_count(ip)
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