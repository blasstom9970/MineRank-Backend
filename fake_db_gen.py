from db_manager import DataBaseManager
import duckdb
from datetime import datetime, timezone
import sqlite3 # DB Base

conn = duckdb.connect('minerank.db')
DB = DataBaseManager(cursor=conn.cursor())
cursor:duckdb.DuckDBPyConnection = DB.cursor  # type: ignore

# 서버 테이블 레코드 추가 생성
cursor.execute("SELECT * FROM servers ORDER BY rank DESC;")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description] # 칼럼 이름

old_data = [dict(zip(columns, row)) for row in rows]# 각 행을 딕셔너리로 변환
print(f"기존 서버 레코드 수: {len(old_data)}")

DB.init_db('servers','''
    ip TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    description TEXT NOT NULL,
    tags TEXT NOT NULL,
    bannerUrl TEXT NOT NULL,
    maxPlayers INTEGER DEFAULT 0,
    online INTEGER DEFAULT 0,
    rank INTEGER DEFAULT 0,
    updated_at TEXT NOT NULL
''')

new_data = []
from server.api_request import get_player_count

for server in old_data:
    # 플레이어 업데이트
    ip = server['ip']
    pl = get_player_count(ip)
    online = server['online'] = pl['online']
    maxp = server['maxPlayers'] = pl['max']

    # 랭크 업데이트를 위한 점수 계산
    occupancy = (online / maxp) if maxp > 0 else 0
    server['_occupancy'] = occupancy

    # 업데이트 시간 갱신
    server['updated_at'] = datetime.now(timezone.utc).isoformat() + 'Z'
    new_data.append(server)

# 정렬: occupancy DESC, online DESC, name ASC
sorted_list = sorted(new_data, key=lambda x: (-x['_occupancy'], -x['online'], x['name']))

# dense rank 부여(동률은 이름 순)
for idx, s in enumerate(sorted_list, start=1):
    s['rank'] = idx
    del s['_occupancy'] # 와 이런 방법도 있네 신기하다

# DB에 반영
for server in sorted_list:
    print(f"Adding server {server}")
    DB.add_entry('servers', server)