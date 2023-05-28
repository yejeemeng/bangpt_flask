from flask import *
from datetime import datetime
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/")
db = client.capstone_design
InfoComments = db['infocomments'] # 정보 게시판
InfoComment_bp = Blueprint('info_comment', __name__)
#--------------------------------------------------------------------------------------------------------------------#
@InfoComment_bp.route('/reg_cmt', methods=['POST'])  # 댓글 작성
def reg_comment():
    userid = request.form['userid']
    content = request.form['content']
    board_seq = request.form['board_seq']
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    
    comment = {
        'userid': userid,
        'content': content,
        'board_seq': board_seq,
        'timestamp' : timestamp
    }

    # 댓글 등록
    InfoComments.insert_one(comment)

    return 'success'


@InfoComment_bp.route('/post', methods=['POST'])# 댓글을 불러옴
def load_cmt():
    board_seq = request.form['board_seq']  # 게시물 ID (요청 파라미터로 전달)

    try:
        comments = InfoComments.find({'board_seq': board_seq})

        result = []
        for comment in comments:
            result.append({'userid': comment['userid'], 
                           'content': comment['content'], 
                           'crt_dt': comment['timestamp']})

        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify([])