class DataBaseManager:
    __shared_state = {}
    
    def __init__(self, cursor = None):
        self.__dict__ = self.__shared_state
        if 'cursor' not in self.__shared_state:
            self.__shared_state['cursor'] = cursor

    def init_db(self, table_name: str, schema: str):
        cursor = self.cursor # type: ignore

        try:
            cursor.execute(f'DROP TABLE {table_name};') # type: ignore
        except:
            pass  # 테이블이 없으면 무시
        cursor.execute(f'''
            CREATE TABLE {table_name} (
                {schema}
            );
        ''') 

    def add_entry(self, table_name: str, data:dict):
        cursor = self.cursor # type: ignore

        columns = ', '.join(data.keys())
        values = ', '.join([f"'{v}'" for v in data.values()])

        cursor.execute(f'''
            INSERT INTO {table_name} ({columns})
            VALUES ({values});
        ''')