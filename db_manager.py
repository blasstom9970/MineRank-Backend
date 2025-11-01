import duckdb
from flask import g
from typing import Optional

class DataBaseManager:
    __shared_state = {}
    
    def __init__(self, db_path: Optional[str] = None):
        self.__dict__ = self.__shared_state
        if 'db_path' not in self.__shared_state and db_path:
            self.__shared_state['db_path'] = db_path

    def get_cursor(self):
        """Get a thread-safe cursor for the current request context"""
        if 'db_cursor' not in g:
            db_path = self.__shared_state.get('db_path')
            if not db_path:
                raise RuntimeError("Database path not configured")
            # Create a new connection for this request
            g.db_connection = duckdb.connect(db_path)
            g.db_cursor = g.db_connection.cursor()
        return g.db_cursor

    def close_connection(self):
        """Close the database connection for the current request"""
        db_cursor = g.pop('db_cursor', None)
        db_connection = g.pop('db_connection', None)
        
        if db_cursor is not None:
            db_cursor.close()
        if db_connection is not None:
            db_connection.close()

    def init_db(self, table_name: str, schema: str):
        cursor = self.get_cursor()

        try:
            cursor.execute(f'DROP TABLE {table_name};')
        except duckdb.CatalogException:
            pass  # 테이블이 없으면 무시
        cursor.execute(f'''
            CREATE TABLE {table_name} (
                {schema}
            );
        ''') 

    def add_entry(self, table_name: str, data:dict):
        # 빈 data면 예외처리 
        if not data:
            raise ValueError("add_entry: 'data'가 비어있습니다.")
        
        cursor = self.get_cursor()
        # 원래는 문자열 그대로 넣었지만 컬럼명/테이블명 만 f-string으로 넣어줌 -> 인젝션 공격 방지
        columns = ', '.join([f'"{k}"' for k in data.keys()])
        
        # 값을 직접 넣지 않고 '?'플레이스홀더로 바꿈
        placeholders = ', '.join(['?'] * len(data))

        # 테이블/컬럼은 포맷, 값은 파라미터로 전달하여 SQL 인젝션 방지
        #f-string보다 테이블 이름을 ""로 감싸주면서 안정성을 높임
        cursor.execute(f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders});', tuple(data.values()))