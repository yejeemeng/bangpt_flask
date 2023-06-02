from datetime import datetime, date
from flask import *
from pymongo import MongoClient
from bson.json_util import dumps
from user_badge import update_attendance

##
#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
Diary = db['diary'] # 다이어리 콜렉션
Attendance= db['attendance']
User_Badges = db['user_badge'] # 유저의 배지 관리 
Badge = db['badges'] # 배지 리스트
Diary_bp = Blueprint('diary', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@Diary_bp.route('/new', methods=['POST']) # 운동 다이어리 추가
def new_diary():

    user_id = request.form['diaryID']
    diary_date = request.form['diaryDate']
    diary_num = Diary.count_documents({"diary_id": user_id, "diary_date": diary_date}) +1
    diary_memo = request.form['diaryMemo']

    diary = {
        'diary_id': user_id,
        'diary_date': diary_date,
        'diary_num': diary_num,
        'diary_memo': diary_memo
    }
    
    # MongoDB에 추가
    Diary.insert_one(diary)
    update_attendance(user_id)
    response = {'success': True}

    return jsonify(response)