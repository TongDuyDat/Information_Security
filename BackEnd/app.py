
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId

app = Flask(__name__)

username = "chukhanhhung"
password = "Abc123"
mongo_uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@cluster0.pvie75s.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client["ABE"] 

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    users_collection = db.USERS
    user = users_collection.find_one({"username": username})

    if user and user['password'] == password:
        session['user_id'] = str(user['_id'])
        return jsonify({"message": "Đăng nhập thành công"})
    else:
        return jsonify({"message": "Tên đăng nhập hoặc mật khẩu không chính xác"})
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Dữ liệu không hợp lệ'}), 400

    new_user = {
        'username': data['username'],
        'password': data['password'],
        'fullname': data.get('fullname', ''),
        'dob': data.get('dob', ''),
        'citizenshipid': data.get('citizenshipid', ''),
        'hometown': data.get('hometown', ''),
        'phonenumber': data.get('phonenumber', ''),
        'key_id': data.get('key_id', '')
    }

    user_collections = db.USERS
    result = user_collections.insert_one(new_user)

    return jsonify({'message': 'Người dùng đã được thêm thành công', 'user_id': str(result.inserted_id)}), 201

@app.route('/delete_user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        obj_id = ObjectId(user_id)

        user_collections = db.USERS
        result = user_collections.delete_one({'_id': obj_id})

        if result.deleted_count == 1:
            return jsonify({'message': 'Người dùng đã được xóa thành công'}), 200
        else:
            return jsonify({'message': 'Không tìm thấy người dùng'}), 404

    except Exception as e:
        return jsonify({'message': 'Lỗi: ' + str(e)}), 500
    
@app.route('/create_post', methods=['POST'])
def create_post():
    data = request.json

    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({"message": "Người dùng chưa đăng nhập"})

    new_post = {
        "user_id": user_id,
        "title": data.get("title"),
        "content": data.get("content"),
        "image": data.get("image")
    }

    posts_collection = db.POSTS
    post_id = str(posts_collection.insert_one(new_post).inserted_id)

    file_collection = db.FILE
    if data.get("link"):
        new_file = {
            "post_id": post_id,
            "link": data.get("link")
        }
        file_collection.insert_one(new_file)

    return jsonify({"message": "Bài viết đã được tạo", "post_id": post_id})
    

@app.route('/edit_post/<string:post_id>', methods=['PUT'])
def edit_post(post_id):
    data = request.json
    user_id = session.get('user_id')
    
    if user_id is None:
        return jsonify({"message": "Người dùng chưa đăng nhập"})

    posts_collection = db.POSTS
    existing_post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if existing_post and existing_post["user_id"] == user_id:
        new_title = data.get("title")
        new_content = data.get("content")
        new_image = data.get("image")

        posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {"title": new_title, "content": new_content, "image": new_image}}
        )

        file_collection = db.FILE
        if data.get("link"):
            new_file = {
                "post_id": post_id,
                "link": data.get("link")
            }
            file_collection.replace_one({"post_id": post_id}, new_file, upsert=True)

        return jsonify({"message": "Bài viết đã được cập nhật"})
    return jsonify({"message": "Không tìm thấy bài viết hoặc bạn không có quyền"})

@app.route('/delete_post/<string:post_id>', methods=['DELETE'])
def delete_post(post_id):
    user_id = session.get('user_id')

    if user_id is None:
        return jsonify({"message": "Người dùng chưa đăng nhập"})

    posts_collection = db.POSTS
    existing_post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if existing_post and existing_post["user_id"] == user_id:
        posts_collection.delete_one({"_id": ObjectId(post_id)})
        file_collection = db.FILE
        file_collection.delete_one({"post_id": post_id})

        return jsonify({"message": "Bài viết đã được xóa"})
    return jsonify({"message": "Không tìm thấy bài viết hoặc bạn không có quyền"})

if __name__ == '__main__':
    app.run(debug=True)