from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import Blueprint

#얘도 아직 미완성...
#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
user_badges = db['badge'] # 유저의 배지 관리 
User_Badge_bp = Blueprint('user_badge', __name__)
#--------------------------------------------------------------------------------------------------------------------#


# API에 유저의 새 배지 추가하기
@User_Badge_bp.route('/post', methods=['POST'])
def add_badge():
    badge_name = request.form['badge_name']
    user_id = request.form['user_id']
    
    badge_date = request.form['badge_date']
    badge = {'badge_name': badge_name, 'user_id': user_id, 'badge_date': badge_date}
    user_badges.insert_one(badge)
    
    return jsonify({'result': '배지 추가 완료~'})


# 유저의 배지 정보 가져오기
@User_Badge_bp.route('/<user_id>', methods=['GET'])
def get_badges(user_id):
    badges = badges.find({'user_id': user_id})
    result = []
    for badge in badges:
        result.append({'badge_name': badge['badge_name'], 'badge_date': badge['badge_date']})
        
    return jsonify(result)