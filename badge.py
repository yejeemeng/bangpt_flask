from flask import Blueprint, request, jsonify,Flask
from bson import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps
import os

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/")
db = client.capstone_design
Badgelist = db["badges"] # 배지 컬렉션에 추가
Badge_bp = Blueprint('badge', __name__) # blueprint 등록
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users/admin/Desktop/rhkwp20231/cd/badgeimage'
#--------------------------------------------------------------------------------------------------------------------#



@Badge_bp.route('/post', methods=['POST'])
def add_badge():
    try:
        badge_name = request.form['badge_name']
        badge_desc = request.form['badge_desc']
        badge_image_url = request.form['badge_image_url']

        # 배지 번호 카운트
        badge_num = Badgelist.count_documents({}) + 1

        badge = {
            'num': badge_num,
            'badge_name': badge_name,
            'badge_desc': badge_desc,
            'badge_image_url' : badge_image_url,
        }

        Badgelist.insert_one(badge)  # MongoDB에 데이터 삽입

        return 'Badge added successfully'

    except Exception as e:
        print(e)
        return jsonify({'success': False})


@Badge_bp.route('/<int:num>', methods=['PUT'])
def update_badge(num):
    badge = Badgelist.find_one({'num': num})
    
    if badge is None:
        return 'no badge'

    badge_name = request.form.get('badge_name', badge['badge_name'])
    badge_desc = request.form.get('badge_desc', badge['badge_desc'])
    badge_image_url = request.form.get('badge_image_url', badge['badge_image_url'])

    # 업로드된 파일 저장
    #if badge_image_url:
    #    filename = badge_image_url.filename
    #   file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #    badge_image_url.save(file_path)

    badge['badge_name'] = badge_name
    badge['badge_desc'] = badge_desc
    badge['badge_image_url'] = badge_image_url


    Badgelist.update_one({'num': num}, {'$set': badge})

    return 'Badge updated successfully'


@Badge_bp.route('/', methods=['GET'])
def get_info_posts():
    cursor = Badgelist.find({})
    badgelists = list(cursor)

    return dumps(badgelists)