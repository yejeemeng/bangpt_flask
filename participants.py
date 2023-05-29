from datetime import datetime
from flask import *
from pymongo import MongoClient
from bson.json_util import dumps

#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
Participants = db['participants'] # 챌린지 참가자 콜렉션
Participants_bp = Blueprint('participants', __name__)
#--------------------------------------------------------------------------------------------------------------------#

@Participants_bp.route('/new', methods=['POST']) # 챌린지 참가자 추가
def new_participant():
    participant_id = request.form['participantId']
    participant_success = request.form['participantSuccess']
    participant_ranking = request.form['participantRanking']
    participant_note = request.form['participantNote']

    # 중복된 참여자인지 확인
    duplicate_participant = Participants.find_one({'participant_id': participant_id})
    if duplicate_participant:
        response = {'success': False}
    else:
        participant = {
            'participant_id': participant_id,
            'participant_success': participant_success,
            'participant_ranking': participant_ranking,
            'participant_note': participant_note
        }
        # MongoDB에 추가
        Participants.insert_one(participant)
        response = {'success': True}

    return jsonify(response)
