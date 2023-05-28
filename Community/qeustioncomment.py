from flask import *
from datetime import datetime
from pymongo import MongoClient
from bson.json_util import dumps

# ~comments 부분은 걍 안 쓰고 post부분에 다 작성할 듯.. 안드로이드에서 코드 고치기 귀찮아ㅜ
#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
QuestionComments = db['questioncomments'] # 질문 게시판
QuestionComment_bp = Blueprint('question_comment', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@QuestionComment_bp.route('/post', methods=['POST'])
def add_question_comment():
    # POST 요청으로 받은 데이터를 파싱
    super_id = request.form['superId']
    title = request.form['title']
    content = request.form['content']
    day = request.form['day']

    # MongoDB에 데이터 저장
    post = {
        'superId': super_id,
        'title': title,
        'content': content,
        'day': day
    }
    QuestionComments.insert_one(post)

    # 클라이언트에게 응답
    return 'Success'

@QuestionComment_bp.route('/', methods=['GET'])
def get_qeustion_comments():
    posts = list(QuestionComments.find({}))
    return jsonify({'question_posts': posts})