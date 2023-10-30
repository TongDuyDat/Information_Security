from flask import Blueprint, request
from database.user_db import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from athu.auth_midde import token_required
from datetime import datetime, timedelta
from config import settings
import jwt
# api 
user_api = Blueprint("user_api", __name__, url_prefix="api")
@user_api.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.get_json()
        user = data["username"]
        passwd = data["password"]
        if User.login(user, passwd):
            token = jwt.encode({
            'username': user,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, settings.SECRET_KEY, algorithm= settings.JWT_ALGORITHM)
            return {"ok": True, "access_token": token}
    return {"ok": False}
@user_api.route("/register", methods =["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = request.get_json()
            if data is None:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            else:
                if data["username"] is None or data["password"] is None or data["fullname"] is None:
                    return {"ok": False}
                user, status = User.register(**data)
                print(user)
                if status:
                    return {"message": "Successfully created new user",
                            "data": user}, 201
                else:
                    return {"message": "User already exists",
                            "data": None,
                            "error": "Bad request"}
        except Exception as e:
            return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500
@user_api.route("/account/<username>")
@token_required
def account(user, username):
    #ham nayf dung dder sur thong tin thong tin nguoi dung
    return {"hello":"heleleleel"}

@user_api.route("/<username>")
@token_required
def user_route(user_id, username):
    #ham nayf lay cac thong tin ve cac nban tin thong tin nguoiw dungf
    return {"hello":user_id}