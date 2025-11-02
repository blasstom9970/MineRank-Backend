from db_manager import DataBaseManager
import duckdb
from server.api_request import get_player_count
from datetime import datetime
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
    Maxplayers INTEGER DEFAULT 0,
    online INTEGER DEFAULT 0,
    rank INTEGER DEFAULT 0,
    updated_at TEXT NOT NULL
''')

new_data = []

for server in old_data:
    # 플레이어 업데이트
    ip = server['ip']
    pl = get_player_count(ip)
    online = server['online'] = pl['online']
    maxp = server['Maxplayers'] = pl['max']

    # 랭크 업데이트를 위한 점수 계산
    occupancy = (online / maxp) if maxp > 0 else 0
    server['_occupancy'] = occupancy

    # 업데이트 시간 갱신
    server['updated_at'] = datetime.utcnow().isoformat() + 'Z'
    new_data.append(server)

# occupancy: 플레이어 수 / 최대 플레이어 수 (max>0), 같으면 online 수로 비교
for s in new_data:
    maxp = s.get('Maxplayers') or 0
    online = s.get('online') or 0
    occupancy = (online / maxp) if maxp > 0 else 0
    s['_occupancy'] = occupancy

# 정렬: occupancy DESC, online DESC
sorted_list = sorted(new_data, key=lambda x: (-x['_occupancy'], -x.get('online', 0)))

# dense rank 부여(동률은 같은 랭크)
rank_counter = 0
prev_key = None
for idx, s in enumerate(sorted_list, start=1):
    key = (round(s['_occupancy'], 8), s.get('online', 0))  # 부동소수점 비교 안전화
    if key != prev_key:
        rank_counter += 1
        prev_key = key
    s['rank'] = rank_counter
    del s['_occupancy'] # 와 이런 방법도 있네 신기하다

# DB에 반영
for server in sorted_list:
    DB.add_entry('servers', server)