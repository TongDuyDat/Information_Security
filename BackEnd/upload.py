from flask import Flask, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus
from werkzeug.utils import secure_filename
import os

username = "chukhanhhung"
password = "Abc123"
mongo_uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@cluster0.pvie75s.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client["ABE"]

UPLOAD_IMG_FOLDER = r'D:/University/Flask_Tutorial/Uploaded/Image'
UPLOAD_FILE_FOLDER = r'D:/University/Flask_Tutorial/Uploaded/File'
ALLOWED_IMG_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])
ALLOWED_FILE_EXTENSIONS = set(['txt', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'xls', 'xlsx'])

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

app = Flask(__name__)
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER
app.config['UPLOAD_FILE_FOLDER'] = UPLOAD_FILE_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"message": "Không tìm thấy tệp"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Không tìm thấy tệp"}), 400
    
    if allowed_file(file.filename, ALLOWED_IMG_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename))
        return jsonify({"message": "Tải lên ảnh thành công"})
    
    elif allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FILE_FOLDER'], filename))
        return jsonify({"message": "Tải lên tệp thành công"})
    else:
        return jsonify({"message": "Phần mở rộng tệp không được hỗ trợ"}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_IMG_FOLDER):
        os.makedirs(UPLOAD_IMG_FOLDER)
    if not os.path.exists(UPLOAD_FILE_FOLDER):
        os.makedirs(UPLOAD_FILE_FOLDER)
    app.run(debug=True)
