# from flask import Flask, request
import os
from flask import *

app = Flask(__name__)
VideoUpload_bp = Blueprint('video_upload', __name__) # 따로 선언하기



UPLOAD_FOLDER = '/Users/estar-kim/Desktop/2023/mju/캡스톤디자인/flask/bangpt-flask_0604/static/video'  # 동영상이 저장될 경로
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@VideoUpload_bp.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No video file in the request', 400

    video_file = request.files['video']
    if video_file.filename == '':
        return 'No selected file', 400

    filename = 'video.mp4'  # 저장할 파일명을 지정.
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video_file.save(save_path)

    return 'Video uploaded successfully'