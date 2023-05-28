from flask import *
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/")
db = client.capstone_design
MyWritings = db['mywritings'] # 내 작성글 볼 수 있는 컬렉션
FreePosts = db['freeposts'] # 자유 게시판
InfoPosts = db['infoposts'] # 정보 게시판
QuestionPosts = db['questionposts'] # 질문 게시판
MyWriting_bp = Blueprint('my_write', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@MyWriting_bp.route('/load_title/<userid>', methods=['POST']) # 마이페이지에서 회원이 작성한 글 볼 수 있게
def load_title(userid):
    try:
        # MongoDB에서 해당 사용자가 작성한 게시물 리스트 조회
        info_boards = InfoPosts.find({'userid': userid})
        free_boards = FreePosts.find({'userid': userid})
        question_boards = QuestionPosts.find({'userid': userid})

        result = []
        
        for board in info_boards:
            result.append({'_id': str(board['_id']), 
                           'title': board['title'], 
                           'content': board['content'], 
                           'timestamp': board['timestamp']
                           })
        
        for board in free_boards:
            result.append({'_id': str(board['_id']), 
                           'title': board['title'], 
                           'content': board['content'], 
                           'timestamp': board['timestamp']
                           })
        
        for board in question_boards:
            result.append({'_id': str(board['_id']), 
                           'title': board['title'], 
                           'content': board['content'], 
                           'timestamp': board['timestamp']
                           })

        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify([])