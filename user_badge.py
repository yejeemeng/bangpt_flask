from flask import Flask, jsonify, request
from datetime import datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import Blueprint

#얘도 아직 미완성...
#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
User_Badges = db['user_badge'] # 유저의 배지 관리 
Badge = db['badges'] # 배지 리스트
Attendance = db['attendance'] # 출석률 확인 컬렉션
Diary = db['diary'] # 다이어리 콜렉션
User_Badge_bp = Blueprint('user_badge', __name__)
#--------------------------------------------------------------------------------------------------------------------#

# 캘린더에 추가됨에 따라 출석 반영(diary_num이 1인 것만 카운트)
def update_attendance(user_id):
    try:
        attendance = Diary.count_documents({'diary_id': user_id, 'diary_num': 1})

        user_attendance = {
            'user_id': user_id,
            'attendance': attendance
        }

        Attendance.update_one({'user_id': user_id}, {'$set': user_attendance}, upsert=True)
        save_attendance(user_id)

    except Exception as e:
        print(e)
    
    
# 유저의 배지 정보 가져오기
@User_Badge_bp.route('/badges', methods=['POST'])
def get_user_badges():
    try:
        user_id = request.form['userID']
        user_document = User_Badges.find_one({'user_id': user_id})
        
        if user_document:
            badges = user_document['badges']
            return jsonify(badges)
        else:
            return jsonify([])
    
    except Exception as e:
        print(e)
        return jsonify([])
    

# 조건에 따라 유저 배지 추가하기
def save_attendance(user_id):
    try:
        attendance = Diary.count_documents({'diary_id': user_id, 'diary_num': 1})

        attendance_document = Attendance.find_one({'user_id': user_id}) 

        # user_id의 출석값을 받아옴
        if attendance_document:
            attendance = attendance_document['attendance']
        else:
            attendance = 0

        # 출석률이 7일을 넘었을 때 배지 1 추가
        if attendance >= 7:
            badge1 = Badge.find_one({'num': 1})
            if badge1:
                # 중복 체크
                existing_badge = User_Badges.find_one({'user_id': user_id, 'badges.badge_num': badge1['num']})
                if not existing_badge:
                    user_badge = {
                        'badge_num': badge1['num'],
                        'badge_name': badge1['badge_name'],
                        'badge_desc': badge1['badge_desc'],
                        'badge_image_url' : badge1['badge_image_url'],
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    user_document = User_Badges.find_one({'user_id': user_id})
                    if user_document:
                        User_Badges.update_one(
                            {'user_id': user_id},
                            {'$push': {'badges': user_badge}}
                        )
                    else:
                        user_document = {
                            'user_id': user_id,
                            'badges': [user_badge]
                        }
                        User_Badges.insert_one(user_document)

        # 출석률이 30일을 넘었을 때 배지 2 추가
        if attendance >= 30:
            badge2 = Badge.find_one({'num': 2})
            if badge2:
                # 중복 체크
                existing_badge = User_Badges.find_one({'user_id': user_id, 'badges.badge_num': badge2['num']})
                if not existing_badge:
                    user_badge = {
                        'badge_num': badge2['num'],
                        'badge_name': badge2['badge_name'],
                        'badge_desc': badge2['badge_desc'],
                        'badge_image_url' : badge2['badge_image_url'],
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    user_document = User_Badges.find_one({'user_id': user_id})
                    if user_document:
                        User_Badges.update_one(
                            {'user_id': user_id},
                            {'$push': {'badges': user_badge}}
                        )
                    else:
                        user_document = {
                            'user_id': user_id,
                            'badges': [user_badge]
                        }
                        User_Badges.insert_one(user_document)
                        
        # 출석률이 30일을 넘었을 때 배지 2 추가..이거 나중에 수정
        if attendance >= 9:
            badge3 = Badge.find_one({'num': 3})
            if badge3:
                # 중복 체크
                existing_badge = User_Badges.find_one({'user_id': user_id, 'badges.badge_num': badge3['num']})
                if not existing_badge:
                    user_badge = {
                        'badge_num': badge3['num'],
                        'badge_name': badge3['badge_name'],
                        'badge_desc': badge3['badge_desc'],
                        'badge_image_url' : badge3['badge_image_url'],
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    user_document = User_Badges.find_one({'user_id': user_id})
                    if user_document:
                        User_Badges.update_one(
                            {'user_id': user_id},
                            {'$push': {'badges': user_badge}}
                        )
                    else:
                        user_document = {
                            'user_id': user_id,
                            'badges': [user_badge]
                        }
                        User_Badges.insert_one(user_document)

        return jsonify({'success' : True})

    except Exception as e:
        print(e)
        return jsonify({'success': False})
