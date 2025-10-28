import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
from db_manager import DataBaseManager
import duckdb

load_dotenv()

# Flask 설정
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)  # 모든 출처 허용. 필요한 경우 특정 도메인만 허용 가능
bcrypt = Bcrypt(app)

# DuckDB 설정
db_path:str = os.getenv("DUCKDB_PATH") # type: ignore
conn = duckdb.connect(db_path)
print(f"Using DuckDB at: {db_path}")
DataBaseManager(cursor=conn.cursor())

# Blueprint 등록
from server import server_bp
from user import user_bp

app.register_blueprint(server_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")