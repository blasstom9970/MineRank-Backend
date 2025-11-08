from duckdb import DuckDBPyConnection

def get_db_dict(cursor:DuckDBPyConnection, command:str) -> list[dict]:
    cursor.execute(command)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] # 칼럼 이름

    db_list = [dict(zip(columns, row)) for row in rows]# 각 행을 딕셔너리로 변환

    return db_list