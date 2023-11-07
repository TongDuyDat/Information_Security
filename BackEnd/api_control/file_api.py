from flask import Blueprint, request, send_file
import os
from datetime import datetime
from config import settings
from database.file_db import File
from database.new_db import Post
api_file = Blueprint("file_api", __name__, url_prefix='api')

EXTENTION_IMG = {'jpg', 'jpeg', 'png', 'gif'}
EXTENTION_DOC = {'txt', 'csv', 'json', 'xml', 'doc', 'pdf', "pptx"}

@api_file.route("/upload_file", methods = ["POST"])
def upload(): 
    try:
        file = request.files['file']
        post_id = request.args.get('post_id')
        
        if file is None:
            return {
                "message": "Please send the correct file",
                "data": None,
                "error": "File is empty"
            }
        if not Post.get_post_by_id(id):
            return {
                "message": "Post does not exist",
                "data": None,
                "error": "Post is empty"
            }
        filenameori = file.filename
        now = datetime.now()
        subfolder = now.strftime('%Y/%m/%d')
        file_extention = filenameori.split(".")[-1]
        save_path = os.path.join(settings.UPLOAD_FOLDER,"File", subfolder)
        dtype = "File"
        if file_extention in EXTENTION_IMG:
            save_path = os.path.join(settings.UPLOAD_FOLDER,"Image", subfolder)
            dtype = "Image"
        elif file_extention in EXTENTION_DOC:
            save_path = os.path.join(settings.UPLOAD_FOLDER,"Doccument", subfolder)
            dtype = "Doccument"
        os.makedirs(save_path, exist_ok=True)
        filename = now.strftime('%Y%m%d%H%M%S')
        path = os.path.join(save_path, filename+ "." + file_extention)
        file.save(path)
        # Save to Database
        status, data = File.create_file(post_id, path, filenameori, filename, dtype)
        data = data.to_json()
        if status:
            return {
                "message": "File uploaded successfully",
                "data": data,           
                }, 200
        else:
            return {
                "message": "Uploading the file failed",
                "data": data,           
                }, 500
    except:
        return {
            "message": "Uploading the file failed",
            "data": None,         
        }, 500
@api_file.route("/get_file", methods = ["GET"])
def get_file():
    id_file = request.args.get("id")
    download = request.args.get("download")
    if not id_file:
        return {"status":"failed","msg":"Id file tidak boleh kosong"},400
    status, data = File.get_file_by_id(id_file)
    if status == True and data != [] :
        if data["type"]=="Image":
            return send_file(data["path"]), 200
        else:
            return send_file(data["path"], as_attachment = download!=None), 200
    return {"status":"failed","msg":"Not Found!"},404