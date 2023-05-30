from datetime import datetime
from flask import *
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
Users = db['user'] # 유저 정보 관리하는 컬렉션
User_Badges = db['user_badge'] # 유저의 배지 관리 
User_bp = Blueprint('user', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@User_bp.route('/join', methods=['POST']) # 회원가입 할 때 사용
def join_user():
    user_id = request.form['userID']
    password = request.form['userPassword']
    name = request.form['userName']
    nickname = request.form['userNick']
    trainer = request.form['trainer']

    # 중복된 아이디인지 확인
    duplicate_user = Users.find_one({'user_id': user_id})
    if duplicate_user:
        response = {'success': False}
    else:
        user = {
            'user_id': user_id,
            'password': password,
            'name': name,
            'nickname': nickname,
            'trainer': trainer
        }
        # MongoDB에 추가
        Users.insert_one(user)
        response = {'success': True}
        
    user_document = {'user_id': user_id, 'badges': []}
    User_Badges.insert_one(user_document)

    return jsonify(response)



@User_bp.route('/chk', methods=['POST']) # id 중복 확인/ ChkIDRequest랑 연결
def check_user_id():
    user_id = request.form['userID']

    # 중복 체크
    duplicate_user = Users.find_one({'user_id': user_id})
    if duplicate_user:
        response = {'success': False}
    else:
        response = {'success': True}

    return jsonify(response)



@User_bp.route('/login', methods=['POST']) # 아이디와 비밀번호를 통해 로그인
def login_user():
    user_id = request.form['userID']
    password = request.form['userPassword']

    # 아이디와 비밀번호로 사용자 확인
    user = Users.find_one({'user_id': user_id, 'password': password})
    if user:
        response = {'success': True}
    else:
        response = {'success': False}

    return jsonify(response)



@User_bp.route('/', methods=['GET']) # 이건 회원 정보 볼 수 있게
def get_info_posts():
    cursor = Users.find({})
    posts = list(cursor)
        
    return dumps(posts)


# 회원정보 / 트레이너 여부 수정, 업데이트 하는 코드
@User_bp.route('/update/<user_id>', methods=['PUT'])
def update_badge(user_id):
    user = Users.find_one({'user_id': user_id})
    
    if user is None:
        return 'User not found'

    user_password = request.form.get('userPassword')
    user_name = request.form.get('userName')
    user_nickname = request.form.get('userNick')
    trainer = request.form.get('trainer')

    if user_password:
        user['password'] = user_password
    if user_name:
        user['name'] = user_name
    if user_nickname:
        user['nickname'] = user_nickname
    if trainer:
        user['trainer'] = trainer

    Users.update_one({'user_id': user_id}, {'$set': user})

    return 'User updated successfully'
