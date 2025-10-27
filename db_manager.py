import os
import duckdb

# DuckDB 설정
db_path:str = os.getenv("DUCKDB_PATH") # type: ignore
print(f"Using DuckDB at: {db_path}")
conn = duckdb.connect(db_path)

#TODO: 각자 다른 table_name에 같은 conn 객체를 쓰게 만들어야 함

class DataBaseManager:
    def __init__(self, table_name:str):
        self.cursor = conn.cursor()
        self.table_name = table_name

    def init_db(self, schema:str):
        try:
            self.cursor.execute(f'DROP TABLE {self.table_name};')
        except:
            pass  # 테이블이 없으면 무시
        self.cursor.execute(f'''
            CREATE TABLE {self.table_name} (
                {schema}
            );
        ''')

    def add_entry(self, data:dict):
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{v}'" for v in data.values()])

        self.cursor.execute(f'''
            INSERT INTO {self.table_name} ({columns})
            VALUES ({values});
        ''')