from flask import Blueprint, jsonify, request
import server.api_request as api
from db_manager import DataBaseManager
import time

bp = Blueprint('server', __name__)
server_db = DataBaseManager()

@bp.route("/servers", methods=['GET', 'POST'])
def servers():
    if request.method == "POST":
        server_db.add_entry('servers', request.get_json())
        return jsonify({"message": "서버 정보가 성공적으로 제출되었습니다."}), 201
    else:  # GET 요청 처리
        server_db.cursor.execute("SELECT * FROM servers ORDER BY rank DESC;") # type: ignore
        server_list = server_db.cursor.fetchall() # type: ignore

        for idx, server in enumerate(server_list):
            if "onlinePlayers" not in server:
                server_list[idx]["onlinePlayers"] = api.get_server_player_count(server["ip"]) # type: ignore

            if "id" not in server:
                server_list[idx]["id"] = idx + 1  # type: ignore
        return jsonify(server_list), 200

@bp.route("/reviews", methods=['GET', 'POST'])
def reviews():
    if request.method == "POST":
        print(request.get_json())
        time.sleep(1)  # 처리 지연 시뮬레이션
        return jsonify({"message": "리뷰가 성공적으로 제출되었습니다."}), 201
    else: # GET 요청 처리
        review_list = []

        for idx, review in enumerate(review_list):
            if "id" not in review:
                review_list[idx]["id"] = idx + 1
        return jsonify(review_list), 200
    
@bp.route("/gallery", methods=['GET', 'POST'])
def gallery():
    return jsonify([
        { "id": 1, "serverId": 1, "user": "gg", "imageUrl": 'https://picsum.photos/seed/gallery1/600/400', "caption": '새로운 성 건축!', "timestamp": '2023-10-25T12:00:00Z' },
        { "id": 2, "serverId": 1, "user": "gg", "imageUrl": 'https://picsum.photos/seed/gallery2/600/400', "caption": '스플리프 토너먼트에서 우승했어요!', "timestamp": '2023-10-24T20:00:00Z' },
        { "id": 3, "serverId": 1, "user": "gg", "imageUrl": 'https://picsum.photos/seed/gallery3/600/400', "caption": '스폰에서 찍은 단체 사진.', "timestamp": '2023-10-23T15:45:00Z' },
        { "id": 4, "serverId": 2, "user": "gg", "imageUrl": 'https://picsum.photos/seed/gallery4/600/400', "caption": '내 건축 부지가 점점 멋져지고 있어요.', "timestamp": '2023-10-26T09:00:00Z' },
        { "id": 5, "serverId": 3, "user": "gg", "imageUrl": 'https://picsum.photos/seed/gallery5/600/400', "caption": '멋진 던전을 발견했어요!', "timestamp": '2023-10-22T22:10:00Z' },
    ]), 200