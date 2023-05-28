from flask import *
from datetime import datetime
from pymongo import MongoClient
from flask import Blueprint

#여기는 완벽한 코드 xxxx 오늘 커뮤니티랑 돌아가면서 완성할 것
#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
User = db['user']
Attendance_bp = Blueprint('attendance', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@Attendance_bp.route('/', methods=['POST'])
def attendance():
    # 요청에서 학생 ID를 가져옴
    user_id = request.form.get('user_id')

    # MongoDB에서 해당 학생의 출석 정보를 가져옴
    user = User.find_one({'user_id': user_id})

    # 해당 학생이 MongoDB에 없는 경우 새로운 문서를 생성
    if user is None:
        user = {'user_id': user_id, 'attendance': []}

    # 출석 정보를 추가하고 MongoDB에 저장
    user['attendance'].append(datetime.now())
    User.save(user)
    
    return jsonify(user)