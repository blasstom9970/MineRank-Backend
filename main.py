import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from db_manager import DataBaseManager
import duckdb

load_dotenv()

# Flask 설정
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app, supports_credentials=True)  # 세션 쿠키를 사용하려면 필수

# DuckDB 설정
db_path:str = os.getenv("DUCKDB_PATH") # type: ignore
conn = duckdb.connect(db_path)
print(f"Using DuckDB at: {db_path}")
DataBaseManager(cursor=conn.cursor())

# Blueprint 등록
from server import server_bp
from user import user_bp
from community import community_bp

app.register_blueprint(server_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(community_bp, url_prefix='/api/community')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")