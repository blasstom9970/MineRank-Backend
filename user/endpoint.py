from flask import blueprints, session, jsonify, request, current_app
from flask_bcrypt import Bcrypt
from db_manager import DataBaseManager
from duckdb import DuckDBPyConnection

bp = blueprints.Blueprint('user', __name__)
# bcrypt = Bcrypt(current_app)

db = DataBaseManager()
cursor:DuckDBPyConnection = db.cursor # type: ignore

db.init_db('users','''
    id INTEGER PRIMARY KEY,
    username TEXT,
    PASSWORD TEXT
''')

@bp.route('/users/')
def get_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall() # 실제 데이터
    columns = [desc[0] for desc in cursor.description] # 칼럼 이름

    users = [dict(zip(columns, row)) for row in rows] # 각 행을 딕셔너리로 변환
    return jsonify(users)

@bp.route('/me')
def get_my_id():
    return "1", 200 #session["user_id"]

@bp.route('/login', methods=['POST'])
def login():
    request.get_json()
    return jsonify({"message": "로그인 기능은 아직 구현되지 않았습니다."}), 501

@bp.route('/signup', methods=['POST'])
def signup():
    return jsonify({"message": "회원가입 기능은 아직 구현되지 않았습니다."}), 501

@bp.route('/delete_account', methods=['POST']) # POST가 다루기 편함
def delete_account():
    return jsonify({"message": "계정 삭제 기능은 아직 구현되지 않았습니다."}), 501