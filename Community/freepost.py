from datetime import datetime
from flask import *
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
FreePosts = db['freeposts'] # 자유 게시판
FreeComments = db['freecomments'] # 자유 게시판 댓글
FreePost_bp = Blueprint('free_post', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@FreePost_bp.route('/post', methods=['POST'])
def add_freepost() :
    userid = request.form.get('userid')
    title = request.form.get('title')
    content = request.form.get('content')
    # 현재 시간 생성
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # MongoDB에 게시물 등록

        board = {
            'userid': userid, 
            'title': title, 
            'content': content,
            'timestamp': timestamp
            }
        result = FreePosts.insert_one(board)

        if result.inserted_id:
            return 'success'
        else:
            return '등록에 실패했습니다.'

    except Exception as e:
        print(e)
        return '등록에 실패했습니다.'



@FreePost_bp.route('/', methods=['GET'])
def get_info_posts():
    cursor = FreePosts.find({})
    posts = list(cursor)
        
    return dumps(posts)


@FreePost_bp.route('/load_board_title/<userid>', methods=['POST']) # commu~post에 list로 넘겨줄 값들
def load_board_title(userid):
    # userid = request.form['userid']  # 사용자 ID (요청 파라미터로 전달)
    
    try:
        # MongoDB에서 게시물 리스트 조회
        # boards = InfoPosts.find({'userid': userid})
        """if userid is None:
            boards = InfoPosts.find({})
        else:
            boards = InfoPosts.find({'userid': userid})"""
        boards = FreePosts.find({})
        result = []
        for board in boards:
            result.append({'_id': str(board['_id']), 
                           'title': board['title'], 
                           'content': board['content'], 
                           'timestamp': board['timestamp']
                           })

        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify([])
    

@FreePost_bp.route('/load_board_detail', methods=['POST']) # WriteviewActivity와 연결
def load_board_detail():
    board_seq = request.form['board_seq']
    board = FreePosts.find_one({'_id': ObjectId(board_seq)})

    if board:
        response = {
            'title': board['title'],
            'content': board['content'],
            'crt_dt': board['timestamp']
        }
    else:
        response = {}

    return jsonify(response)



@FreePost_bp.route('/load_cmt', methods=['POST']) # 댓글을 불러옴
def load_cmt():
    board_seq = request.form['board_seq']  # 게시물 ID (요청 파라미터로 전달)

    try:
        comments = FreeComments.find({'board_seq': board_seq})

        result = []
        for comment in comments:
            result.append({'userid': comment['userid'], 
                           'content': comment['content'], 
                           'crt_dt': comment['timestamp']})

        return jsonify(result)

    except Exception as e:
        print(e)
        return jsonify([])
    

@FreePost_bp.route('/reg_cmt', methods=['POST'])  # 댓글 작성
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
    FreeComments.insert_one(comment)

    return 'success'
