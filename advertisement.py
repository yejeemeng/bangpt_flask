from flask import *
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/")
db = client.capstone_design
Advertisement = db['advertisement'] # 광고 정보 저장 게시판
Advertisement_bp = Blueprint('advertisement', __name__) # blueprint 등록
#--------------------------------------------------------------------------------------------------------------------#

@Advertisement_bp.route('/post', methods=['POST'])
def add_advertisement():

    user_id = request.form['user_id']
    start = datetime.now()
    start_date = start.strftime('%Y-%m-%d %H:%M:%S')
    end_date = start + timedelta(days = 14)
    
    advertisements = {
        "user_id" : user_id,
        "start_date" : start_date,
        "end_date" : end_date,
    }
    
    # 출석 정보를 추가하고 MongoDB에 저장
    Advertisement.insert_one(advertisements)
    
    return 'advertisement added successfully'

@Advertisement_bp.route('/', methods=['GET'])
def get_info_posts():
    cursor = Advertisement.find({})
    adver = list(cursor)

    return dumps(adver)