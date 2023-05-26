from flask import Flask, request, jsonify
from pymongo import MongoClient
import random
import json
import requests

app = Flask(__name__)

client = MongoClient('mongodb+srv://yejeemeng:bangPT@bangpt.hqlexmy.mongodb.net/?retryWrites=true&w=majority')
# mongodb+srv://yejee:yejeejudy@cluster0.q7jgle8.mongodb.net/
db = client['bangPT']
collection = db['user']

data = {"name": "John", "age": 30}

@app.route('/', methods=['GET'])
def index():
    data = collection.find_one({'name':'안은비'})
    print(request.args)
    return f"{data['nickname']}"

@app.route('/join/', methods=['POST'])
def join():
   
    data = request.get_json()

    print("user 콜렉션에 새 도큐멘트 추가")
    print(data)
    result = collection.insert_one(data)

    # 안드로이드에 보낼 응답 데이터 생성
    if result.inserted_id:
        response_data = {
            'success': True,
            'message': '회원가입이 성공적으로 완료되었습니다.'
        }
    else:
        response_data = {
            'success': False,
            'message': '회원가입에 실패하였습니다.'
        }

    return jsonify(response_data)

# @app.route('/chkId/', methods=['GET','POST'])
# def chkId():
    
#     repeated = False
#     data = request.get_json()

#     print("ID 중복 확인")
#     print(data)

#     for document in collection:
#         print(document["id"])
#         if data["id"] == document["id"]:
#             repeated = True

#     # 안드로이드에 보낼 응답 데이터 생성
#     if repeated:
#         response_data = {
#             'repeated': True,
#             'message': '이미 존재하는 ID입니다.'
#         }
#     else:
#         response_data = {
#             'repeated': False,
#             'message': '사용 가능한 ID입니다.'
#         }

#     return jsonify(response_data)

@app.route('/test/')
def test():
    # data = {
    #     'id':'yejeemeng'
    # }

    # print(data)
    print(23)

  #  cnt = collection.find({'id':'yejeemeng'}).count()
    # cnt = collection.count_documents({'id':'yejeemeng'})
    # print(cnt)
  #      if data["id"] == document["id"]:
  #          repeated = True
#     # 안드로이드에 보낼 응답 데이터 생성
#     if repeated:
#         response_data = {
#             'repeated': True,
#             'message': '이미 존재하는 ID입니다.'
#         }
#     else:
#         response_data = {
#             'repeated': False,
#             'message': '사용 가능한 ID입니다.'
#         }
    
    return f"{23}"



if __name__ == "__main__" :
    app.run(debug=True)
 