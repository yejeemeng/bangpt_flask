from datetime import datetime
from flask import *
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/")
db = client.capstone_design
Exercise_result = db['exercise_result'] # 유저 정보 관리하는 컬렉션
Users = db['users'] # 유저의 배지 관리 
Exercise_result_bp = Blueprint('exercise_result', __name__)
#--------------------------------------------------------------------------------------------------------------------#

    

@Exercise_result_bp.route('/<userid>', methods=['POST'])
def get_info_posts(userid):
    try:
        #user_id = request.json['userid']
        #num = int(request.json['num'])
        
        result = Exercise_result.find_one({'user_id': userid})

        if result:
            response = {
                "Reps1": result['score_100'][0],
                "Reps2": result['score_100'][1],
                "Reps3": result['score_100'][2],
                "Reps4": result['score_100'][3],
                "Reps5": result['score_100'][4],
                "score_100_total": result['score_100_total'],
                "best_reps": result['best_rep'],
                "worst_reps": result['worst_rep'],
                "feedback": result['feedback'],
                "timestamp": result['timestamp']
            }
            return jsonify(response)
        
        else:
            return jsonify({})

    except Exception as e:
        print(e)
        return jsonify([])

    
    except Exception as e:
        print(e)
        return jsonify([])