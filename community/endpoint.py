from flask import Blueprint, jsonify, request, session
from db_manager import DataBaseManager
from duckdb import DuckDBPyConnection
from datetime import datetime

bp = Blueprint('community', __name__)
db = DataBaseManager()
cursor: DuckDBPyConnection = db.cursor  # type: ignore

# community_posts 테이블 생성 (데이터 유지)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS community_posts (
        id INTEGER PRIMARY KEY,
        serverId INTEGER NOT NULL,
        userId INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        views INTEGER DEFAULT 0,
        recommendations INTEGER DEFAULT 0
    );
''')

# community_comments 테이블 생성 (데이터 유지)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS community_comments (
        id INTEGER PRIMARY KEY,
        postId INTEGER NOT NULL,
        userId INTEGER NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
''')


def _get_user_info(user_id: int):
    """사용자 정보 조회 헬퍼 함수"""
    cursor.execute("SELECT id, username FROM users WHERE id = ?", [user_id])
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "username": row[1], "password": ""}
    return None


@bp.route("/posts", methods=['GET', 'POST'])
def posts():
    if request.method == "POST":
        # 로그인 확인
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "UNAUTHORIZED"}), 401
        
        data = request.get_json(silent=True) or {}
        server_id = data.get('serverId')
        title = (data.get('title') or '').strip()
        content = (data.get('content') or '').strip()
        
        if not title or not content or not server_id:
            return jsonify({"error": "MISSING_FIELDS"}), 400
        
        # 게시물 생성 - 먼저 다음 ID 계산
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM community_posts")
        next_id_result = cursor.fetchone()
        next_id = next_id_result[0] if next_id_result else 1
        
        timestamp = datetime.utcnow().isoformat() + 'Z'
        cursor.execute(
            '''INSERT INTO community_posts (id, serverId, userId, title, content, timestamp, views, recommendations)
               VALUES (?, ?, ?, ?, ?, ?, 0, 0)''',
            [next_id, server_id, user_id, title, content, timestamp]
        )
        
        # 생성된 게시물 조회
        cursor.execute(
            "SELECT id, serverId, userId, title, content, timestamp, views, recommendations FROM community_posts WHERE id = ?",
            [next_id]
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "POST_CREATE_FAILED"}), 500
        
        user_info = _get_user_info(user_id)
        
        # 댓글 수 계산
        cursor.execute("SELECT COUNT(*) FROM community_comments WHERE postId = ?", [row[0]])
        count_result = cursor.fetchone()
        comment_count = count_result[0] if count_result else 0
        
        post = {
            "id": row[0],
            "serverId": row[1],
            "user": user_info,
            "title": row[3],
            "content": row[4],
            "timestamp": row[5],
            "views": row[6],
            "recommendations": row[7],
            "commentCount": comment_count
        }
        
        return jsonify(post), 201
        
    else:  # GET 요청 처리
        server_id = request.args.get('serverId', type=int) # 쿼리 파라미터로 serverId 필터링 가능
        
        if server_id:
            cursor.execute(
                "SELECT id, serverId, userId, title, content, timestamp, views, recommendations FROM community_posts WHERE serverId = ? ORDER BY id DESC",
                [server_id]
            )
        else:
            cursor.execute(
                "SELECT id, serverId, userId, title, content, timestamp, views, recommendations FROM community_posts ORDER BY id DESC"
            )
        
        rows = cursor.fetchall()
        posts_list = []
        
        for row in rows:
            post_id = row[0]
            user_info = _get_user_info(row[2])
            
            # 댓글 수 계산
            cursor.execute("SELECT COUNT(*) FROM community_comments WHERE postId = ?", [post_id])
            count_result = cursor.fetchone()
            comment_count = count_result[0] if count_result else 0
            
            posts_list.append({
                "id": post_id,
                "serverId": row[1],
                "user": user_info,
                "title": row[3],
                "content": row[4],
                "timestamp": row[5],
                "views": row[6],
                "recommendations": row[7],
                "commentCount": comment_count
            })
        
        return jsonify(posts_list), 200


@bp.route("/comments", methods=['GET', 'POST'])
def comments():
    if request.method == "POST":
        # 로그인 확인
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "UNAUTHORIZED"}), 401
        
        data = request.get_json(silent=True) or {}
        post_id = data.get('postId')
        content = (data.get('content') or '').strip()
        
        if not post_id or not content:
            return jsonify({"error": "MISSING_FIELDS"}), 400
        
        # 게시물 존재 확인
        cursor.execute("SELECT 1 FROM community_posts WHERE id = ?", [post_id])
        if not cursor.fetchone():
            return jsonify({"error": "POST_NOT_FOUND"}), 404
        
        # 댓글 생성 - 먼저 다음 ID 계산
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM community_comments")
        next_id_result = cursor.fetchone()
        next_id = next_id_result[0] if next_id_result else 1
        
        timestamp = datetime.utcnow().isoformat() + 'Z'
        cursor.execute(
            '''INSERT INTO community_comments (id, postId, userId, content, timestamp)
               VALUES (?, ?, ?, ?, ?)''',
            [next_id, post_id, user_id, content, timestamp]
        )
        
        # 생성된 댓글 조회
        cursor.execute(
            "SELECT id, postId, userId, content, timestamp FROM community_comments WHERE id = ?",
            [next_id]
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "COMMENT_CREATE_FAILED"}), 500
        
        user_info = _get_user_info(user_id)
        
        comment = {
            "id": row[0],
            "postId": row[1],
            "user": user_info,
            "content": row[3],
            "timestamp": row[4]
        }
        
        return jsonify(comment), 201
        
    else:  # GET 요청 처리
        # 쿼리 파라미터로 postId 필터링 가능
        post_id = request.args.get('postId', type=int)
        
        if post_id:
            cursor.execute(
                "SELECT id, postId, userId, content, timestamp FROM community_comments WHERE postId = ? ORDER BY id ASC",
                [post_id]
            )
        else:
            cursor.execute(
                "SELECT id, postId, userId, content, timestamp FROM community_comments ORDER BY id ASC"
            )
        
        rows = cursor.fetchall()
        comments_list = []
        
        for row in rows:
            user_info = _get_user_info(row[2])
            
            comments_list.append({
                "id": row[0],
                "postId": row[1],
                "user": user_info,
                "content": row[3],
                "timestamp": row[4]
            })
        
        return jsonify(comments_list), 200