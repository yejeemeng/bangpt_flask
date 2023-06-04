from datetime import datetime, date
from flask import *
from pymongo import MongoClient
from bson.json_util import dumps
from user_badge import update_attendance

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

@Diary_bp.route('/get/<diary_id>/<diary_date>', methods=['GET']) # 해당일의 운동 다이어리 읽어들이기
def get_diary(diary_id, diary_date):

    cursor = Diary.find({"diary_id": diary_id, "diary_date": diary_date})
    print(diary_id)
    print(diary_date)

    memos = list(cursor)
    return dumps(memos)

@Diary_bp.route('/get/<diary_id>/<diary_year>/<diary_month>', methods=['GET']) # 해당 월의 운동한 날짜 읽어들이기
def get_date(diary_id, diary_year, diary_month):

    string = diary_year + "-" + f"{int(diary_month):02}"
    cursor = Diary.find({"diary_id": diary_id , "diary_num": 1, "diary_date": {"$regex" : string}})

    exercise_dates = list(cursor) #해당 월에 운동한 날들에 해당하는 도큐멘트
    return dumps(exercise_dates)