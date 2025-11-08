from flask import Blueprint, jsonify, request
import server.updater as updater
from db_manager import DataBaseManager
from duckdb import DuckDBPyConnection
from get_db_dict import get_db_dict
import time

bp = Blueprint('server', __name__)
db = DataBaseManager()
cursor:DuckDBPyConnection = db.cursor # type: ignore

@bp.route("/servers", methods=['GET', 'POST'])
def servers():
    if request.method == "POST":
        # 새로운 서버 추가
        server = updater.add_new_server(request.get_json())
        db.add_entry("servers", server)

        # 플레이어 수 갱신
        server_list = get_db_dict(cursor, "SELECT * FROM servers ORDER BY rank DESC;")
        updater.update_player_counts(cursor, server_list)

        updater.update_servers_rank(cursor) # 랭크 갱신
        return jsonify({"message": "서버 정보가 성공적으로 제출되었습니다."}), 201
    else:  # GET 요청 처리
        server_list = get_db_dict(cursor, "SELECT * FROM servers ORDER BY rank DESC;")
        return jsonify(server_list), 200

@bp.route("/reviews", methods=['GET', 'POST'])
def reviews():
    if request.method == "POST":
        print(request.get_json())
        time.sleep(1)  # 처리 지연 시뮬레이션
        return jsonify({"message": "리뷰가 성공적으로 제출되었습니다."}), 201
    else: # GET 요청 처리
        review_list = get_db_dict(cursor, "SELECT * FROM review;")

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
        gallery_list = get_db_dict(cursor, "SELECT * FROM gallery;")
        return jsonify(gallery_list), 200