from datetime import datetime, date
from flask import *
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
Diary = db['diary'] # 다이어리 콜렉션
Diary_bp = Blueprint('diary', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@Diary_bp.route('/new', methods=['POST']) # 운동 다이어리 추가
def new_diary():

    diary_id = request.form['diaryID']
    diary_date = request.form['diaryDate']
    diary_num = Diary.count_documents({"diary_id": diary_id, "diary_date": diary_date}) +1
    diary_memo = request.form['diaryMemo']

    diary = {
        'diary_id': diary_id,
        'diary_date': diary_date,
        'diary_num': diary_num,
        'diary_memo': diary_memo
    }
    # MongoDB에 추가
    Diary.insert_one(diary)
    response = {'success': True}

    return jsonify(response)

@Diary_bp.route('/get/<diary_id>/<diary_date>', methods=['GET']) # 해당일의 운동 다이어리 읽어들이기
def get_diary(diary_id, diary_date):

    cursor = Diary.find({"diary_id": diary_id, "diary_date": diary_date})
    print(diary_id)
    print(diary_date)

    memos = list(cursor)
    return dumps(memos)