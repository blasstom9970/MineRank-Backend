from flask import Blueprint, jsonify, request
import server.api_request as api
from db_manager import DataBaseManager
import time

bp = Blueprint('server', __name__)
db = DataBaseManager()

server_list = [] # 이어서 불러올 수 있도록 전역변수 화

@bp.route("/servers", methods=['GET', 'POST'])
async def servers():
    global server_list

    if request.method == "POST":
        db.add_entry('servers', request.get_json())
        return jsonify({"message": "서버 정보가 성공적으로 제출되었습니다."}), 201
    else:  # GET 요청 처리
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM servers ORDER BY rank DESC;")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] # 칼럼 이름

        server_list += [dict(zip(columns, row)) for row in rows][len(server_list):] # 각 행을 딕셔너리로 변환

        for idx, server in enumerate(server_list):
            if "onlinePlayers" not in server:
                server_list[idx]["onlinePlayers"] = await api.get_server_player_count(server["ip"]) # type: ignore

            if "id" not in server:
                server_list[idx]["id"] = idx + 1  # type: ignore

            if type(server["tags"]) == str:
                server["tags"] = server["tags"].split(",")
        return jsonify(server_list), 200

@bp.route("/reviews", methods=['GET', 'POST'])
def reviews():
    if request.method == "POST":
        print(request.get_json())
        time.sleep(1)  # 처리 지연 시뮬레이션
        return jsonify({"message": "리뷰가 성공적으로 제출되었습니다."}), 201
    else: # GET 요청 처리
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM review;")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] # 칼럼 이름

        review_list = [dict(zip(columns, row)) for row in rows][len(server_list):] # 각 행을 딕셔너리로 변환

        for idx, review in enumerate(review_list):
            if "id" not in review:
                review_list[idx]["id"] = idx + 1
        return jsonify(review_list), 200
    
@bp.route("/gallery", methods=['GET', 'POST'])
def gallery():
    if request.method == "POST":
        print(request.get_json())
        time.sleep(1)  # 처리 지연 시뮬레이션
        return jsonify({"message": "갤러리 게시물이 성공적으로 제출되었습니다."}), 201
    else:
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM gallery;")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] # 칼럼 이름

        gallery_list = [dict(zip(columns, row)) for row in rows][len(server_list):] # 각 행을 딕셔너리로 변환

        return jsonify(gallery_list), 200