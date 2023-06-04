from flask import Flask
from pymongo import MongoClient
from user import User_bp
from participants import Participants_bp
from diary import Diary_bp
from trainers import Trainers_bp
from Community.freepost import FreePost_bp
from Community.infopost import InfoPost_bp
from Community.questionpost import QuestionPost_bp
from Community.freecomment import FreeComment_bp
from Community.infocomment import InfoComment_bp
from Community.questioncomment import QuestionComment_bp
from advertisement import Advertisement_bp
from badge import Badge_bp
from mywrite import MyWriting_bp
from diary import Diary_bp

# (추가)
from user_badge import User_Badge_bp
from videoUpload import VideoUpload_bp
from model import Model_bp

# --------------------------------------- mongoDB : capstone_design 연결----------------------------------------------#
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/' 
client = MongoClient(app.config['MONGO_URI'])
db = client.capstone_design
# --------------------------------------------------------------------------------------------------------------------#
# UPLOAD_FOLDER = r'C:\Users\admin\Desktop\rhkwp20231\cd\badgeimage'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER = '/Users/estar-kim/Desktop/2023/mju/캡스톤디자인/flask/practice6/static/assets/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(User_bp, url_prefix='/user')
app.register_blueprint(Participants_bp, url_prefix='/participants')
app.register_blueprint(Trainers_bp, url_prefix='/trainers')
app.register_blueprint(FreePost_bp, url_prefix='/freepost')
app.register_blueprint(FreeComment_bp, url_prefix='/freecomment')
app.register_blueprint(QuestionPost_bp, url_prefix='/questionpost')
app.register_blueprint(QuestionComment_bp, url_prefix='/questioncomment')
app.register_blueprint(InfoPost_bp, url_prefix='/infopost')
app.register_blueprint(InfoComment_bp, url_prefix='/infocomment')
app.register_blueprint(Diary_bp, url_prefix='/diary')
app.register_blueprint(Badge_bp, url_prefix='/badge')
app.register_blueprint(User_Badge_bp, url_prefix='/userbadge')
app.register_blueprint(Advertisement_bp, url_prefix='/advertisement')
app.register_blueprint(MyWriting_bp, url_prefix='/mywriting')

# (추가)
app.register_blueprint(VideoUpload_bp, url_prefix='/upload')
app.register_blueprint(Model_bp, url_prefix='/model')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=821, debug=True)