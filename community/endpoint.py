from flask import Blueprint, jsonify, request
from db_manager import DataBaseManager

bp = Blueprint('community', __name__)
server_db = DataBaseManager()

@bp.route("/posts", methods=['GET', 'POST'])
def posts():
    if request.method == "POST":
        return jsonify({"message": "새 게시물이 성공적으로 제출되었습니다."}), 201
    else:  # GET 요청 처리
        return jsonify(["server_list"]), 200
    
@bp.route("/comments", methods=['GET', 'POST'])
def comments(): #함수이름이 댓글이니까 댓글에 맞게 message 변경
    if request.method == "POST":
        return jsonify({"message": "새 댓글이 성공적으로 개시되었습니다."}), 201
    else:  # GET 요청 처리
        return jsonify(["server_list"]), 200
