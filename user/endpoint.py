from flask import blueprints, session, jsonify, request, current_app
from flask_bcrypt import Bcrypt
from db_manager import DataBaseManager
from duckdb import DuckDBPyConnection

bp = blueprints.Blueprint('user', __name__)

# Flask-Bcrypt: 앱 컨텍스트에서 동작하므로 전역 인스턴스만 생성
bcrypt = Bcrypt()

db = DataBaseManager()
cursor:DuckDBPyConnection = db.cursor # type: ignore

# db.init_db('users','''
#     id INTEGER PRIMARY KEY,
#     username TEXT,
#     PASSWORD TEXT
# ''')

@bp.route('/users/')
def get_users():
    # 비밀번호는 반환하지 않음 (기존 경로 유지)
    cursor.execute("SELECT id, username FROM users")
    rows = cursor.fetchall()
    users = [{"id": r[0], "username": r[1]} for r in rows]
    return jsonify(users)

@bp.route('/auth/me')
def get_my_id():
    if "user_id" in session:
        return str(session["user_id"]), 200
    else:
        return "-1", 200

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '')

    if not username or not password:
        return jsonify({"error": "USERNAME_OR_PASSWORD_MISSING"}), 400

    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", [username])
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "INVALID_CREDENTIALS"}), 401

    stored_hash = row[2] or ''
    if not bcrypt.check_password_hash(stored_hash, password):
        return jsonify({"error": "INVALID_CREDENTIALS"}), 401

    session['user_id'] = int(row[0])
    return jsonify({"id": int(row[0]), "username": row[1]}), 200

@bp.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '')

    if not username or not password:
        return jsonify({"error": "USERNAME_OR_PASSWORD_MISSING"}), 400

    # 중복 체크
    cursor.execute("SELECT 1 FROM users WHERE username = ?", [username])
    if cursor.fetchone():
        return jsonify({"error": "USERNAME_TAKEN"}), 409

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    count = cursor.execute("SELECT COUNT(*) FROM users;")
    count = int(count.fetchone()[0]) + 1 # type: ignore
    cursor.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", [count, username, pw_hash])

    # 생성된 사용자 조회
    cursor.execute("SELECT id, username FROM users WHERE username = ?", [username])
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "SIGNUP_FAILED"}), 500

    session['user_id'] = int(row[0])
    return jsonify({"id": int(row[0]), "username": row[1]}), 201

@bp.route('/auth/logout', methods=['POST']) # POST가 다루기 편함
def logout():
    session.pop('user_id', None)
    return jsonify({"ok": True}), 200