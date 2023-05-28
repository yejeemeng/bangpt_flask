from flask import *
from datetime import datetime
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
FreeComments = db['freecomments'] # 자유 게시판
FreeComment_bp = Blueprint('free_comment', __name__)
#--------------------------------------------------------------------------------------------------------------------#

FreeComment_bp = Blueprint('free_comment', __name__)
@FreeComment_bp.route('/post', methods=['POST'])
def add_free_comment() :
    
    # Request에서 데이터 추출
    title = request.json['title']
    content = request.json['content']
    
    # 현재 시간 생성
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # 게시물 생성
    comment = {
        'title': title,
        'timestamp': timestamp,
        'content': content
    }
    
    # MongoDB에 추가
    FreeComments.insert_one(comment)

    # 클라이언트에게 응답
    return 'Success'


@FreeComment_bp.route('/', methods=['GET'])
def get_info_posts():
    cursor = FreeComments.find({})
    posts = list(cursor)
        
    return dumps(posts)