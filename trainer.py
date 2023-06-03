import base64
from gettext import npgettext
import io
from pprint import isreadable
from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import os
from flask_cors import CORS


#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
Trainers = db['trainers'] # 다이어리 콜렉션
Trainers_bp = Blueprint('trainers', __name__)
app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\admin\\Desktop\\rhkwp20231\\cd\\badgeimage'
#--------------------------------------------------------------------------------------------------------------------#

@Trainers_bp.route('/get_photo', methods=['POST'])
def upload():
    
    if 'image' in request.files:
        image = request.files['image']
        filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return {'message': 'Image uploaded successfully.'}
    else:
        return {'message': 'No image found in request.'}