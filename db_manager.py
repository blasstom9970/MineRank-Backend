class DataBaseManager:
    __shared_state = {}
    
    def __init__(self, cursor = None):
        # 공유 상태로 동기화
        self.__dict__ = self.__shared_state
        if 'cursor' not in self.__shared_state:
            self.__shared_state['cursor'] = cursor
            print("DataBaseManager 인스턴스가 생성되었습니다.")
            print(f"Cursor: {self.__shared_state['cursor']}")

    @property
    def cursor(self):
        return self.__shared_state['cursor']

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
        # 빈 data면 예외처리 
        if not data:
            raise ValueError("add_entry: 'data'가 비어있습니다.")
        
        cursor = self.cursor # type: ignore
        # 원래는 문자열 그대로 넣었지만 컬럼명/테이블명 만 f-string으로 넣어줌 -> 인젝션 공격 방지
        columns = ', '.join([f'"{k}"' for k in data.keys()])
        
        # 값을 직접 넣지 않고 '?'플레이스홀더로 바꿈
        placeholders = ', '.join(['?'] * len(data))

        # 테이블/컬럼은 포맷, 값은 파라미터로 전달하여 SQL 인젝션 방지
        #f-string보다 테이블 이름을 ""로 감싸주면서 안정성을 높임
        cursor.execute(f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders});', tuple(data.values()))