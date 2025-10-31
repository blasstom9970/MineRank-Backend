import os
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from db_manager import DataBaseManager
import duckdb

load_dotenv()

# Flask 설정
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# CORS 설정: 환경 변수에서 허용 origin 목록을 읽어와 credentials 포함 허용
raw_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in raw_cors_origins.split(",") if origin.strip()]
app.config["CORS_SUPPORTS_CREDENTIALS"] = True
app.config["CORS_ALLOW_HEADERS"] = ["Content-Type", "Authorization"]

allowed_origins_set = set(allowed_origins)

CORS(
    app,
    origins=allowed_origins,
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)

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