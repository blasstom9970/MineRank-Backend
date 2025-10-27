from flask import blueprints, current_app, jsonify, request

bp = blueprints.Blueprint('user', __name__)

@bp.route('/users/')
def get_users():
    # 예시 사용자 데이터
    users = [
        { "id": 1, "username": '스티브' },
        { "id": 2, "username": '알렉스' },
        { "id": 3, "username": '크리퍼팬' },
        { "id": 4, "username": '엔더맨러버' },
    ]
    return jsonify(users)

@bp.route('/login', methods=['POST'])
def login():
    request.get_json()
    return jsonify({"message": "로그인 기능은 아직 구현되지 않았습니다."}), 501

@bp.route('/signup', methods=['POST'])
def signup():
    return jsonify({"message": "회원가입 기능은 아직 구현되지 않았습니다."}), 501

@bp.route('/delete_account', methods=['DELETE'])
def delete_account():
    return jsonify({"message": "계정 삭제 기능은 아직 구현되지 않았습니다."}), 501