from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import os


#--------------------------------------------------------------------------------------------------------------------#
client = MongoClient("mongodb://localhost:27017/hyeyeon?retryWrites=true&w=majority")
db = client.capstone_design
Trainers = db['trainers'] # 다이어리 콜렉션
Trainers_bp = Blueprint('trainers', __name__)
app = Flask(__name__)
app.config.from_object(__name__)
#--------------------------------------------------------------------------------------------------------------------#

UPLOAD_FOLDER = r'D:/workspace/vscode/bang-pt/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@Trainers_bp.route('/get-photo', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        filename = image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {'message': 'Image uploaded successfully.'}, 200
    else:
        return {'message': 'No image found in request.'}, 400