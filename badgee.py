from flask import Blueprint, request, jsonify
from bson import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/")
db = client.capstone_design
Badgelist = db["badges"] # 배지 컬렉션에 추가
Badge_bp = Blueprint('badge', __name__) # blueprint 등록
#--------------------------------------------------------------------------------------------------------------------#

count = 0

@Badge_bp.route('/post', methods=['POST'])
def add_badge():
    global count
    count += 1

    badge_name = request.form['badge_name']
    badge_desc = request.form['badge_desc']
    #badge_image = request.files['badge_image']
    
    # 이미지 파일 저장
    #badge_image = request.form['badge_image']

    badge = {
        'num': (count),
        'badge_name': badge_name,
        'badge_desc': badge_desc,
        #'badge_image' : badge_image,
    }

    Badgelist.insert_one(badge)  # MongoDB에 데이터 삽입

    return 'Badge added successfully '


@Badge_bp.route('/<int:num>', methods=['PUT'])
def update_badge(num):
    badge = Badgelist.find_one({'num': num})
    if badge is None:
        return 'Badge not found'

    badge_name = request.form.get('badge_name', badge['badge_name'])
    badge_desc = request.form.get('badge_desc', badge['badge_desc'])
    #badge_image_url = request.form.get('badge_image_url', badge['badge_image_url'])

    badge['badge_name'] = badge_name
    badge['badge_desc'] = badge_desc
    #badge['badge_image_url'] = badge_image_url

    Badgelist.update_one({'num': num}, {'$set': badge})

    return 'Badge updated successfully'


@Badge_bp.route('/', methods=['GET'])
def get_info_posts():
    cursor = Badgelist.find({})
    badgelists = list(cursor)

    return dumps(badgelists)