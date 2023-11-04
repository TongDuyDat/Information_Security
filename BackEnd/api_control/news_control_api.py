from flask import Blueprint, request, session, jsonify, send_file
from athu.auth_midde import token_required
from database.new_db import Post
import os
from datetime import datetime
from werkzeug.utils import secure_filename

new_api = Blueprint("new_api", __name__, url_prefix="api")

@new_api.route("/create_post", methods=["GET", "POST"])
@token_required
def create_post(user_id):
    if user_id is not None:
        try:
            data = request.get_json()
            if data is None:
                return {
                    "message": "Please provide post details",
                    "data": None,
                    "error": "Bad request"
                }, 400
            else:
                if "title" not in data or "content" not in data or "post_type" not in data:
                    return {
                        "message": "Please provide title, content and type of post in the request data",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                print("Data:", data)
                post, status = Post.create_post(user_id, **data)
                if status:
                    return {
                        "message": "Post successfully created",
                        "data": {"post_id ": str(post.id)}
                    }, 201
                else:
                    return {
                        "message": "Post already exists",
                        "data": None,
                        "error": "Bad request"
                    }, 400
        except Exception as e:
            return {
                "message": "Something went wrong",
                "error": str(e),
                "data": None
            }, 500
    else:
        return {
            "message": "User not logged in",
            "data": None,
            "error": "Unauthorized"
        }, 401
    
@new_api.route("/get_posts", methods=["GET"])
@token_required
def get_posts(user_id):
    if user_id is not None:
        post, status = Post.get_all_post()
        if status:
            return {
                "message": "All posts fetched successfully",
                "data": post,
                }
        return {
                "message": "Fail",
                "data": None,
                }, 401
    return {
            "message": "User not logged in",
            "data": None,
            "error": "Unauthorized"
        }, 401

@new_api.route("/search_posts", methods=["GET", "POST"])
@token_required
def search_posts(user_id):
    if user_id is not None:
        try:
            query = request.args.get("query")
                
            if query is None:
                return {
                    "message": "Please provide a query parameter for search",
                    "data": None,
                    "error": "Bad request"
                }, 400
            
            posts, status = Post.search_posts(query)
            
            if status:
                return {
                    "message": "Search results fetched successfully",
                    "data": posts
                }
            
            return {
                "message": "No matching posts found",
                "data": None
            }
        except Exception as e:
                return {
                    "message": "Something went wrong",
                    "error": str(e),
                    "data": None
                }, 500
    else:
        return {
                "message": "User not logged in",
                "data": None,
                "error": "Unauthorized"
        }, 401
    
@new_api.route("/update_post/<post_id>", methods=["PUT"])
@token_required
def update_post(user_id, post_id):
    if user_id is not None:
        data = request.get_json()
        if data is None:
            return {
                "message": "Please provide post details",
                "data": None,
                "error": "Bad request"
            }, 400

        if Post.update_post(post_id, user_id, **data):
            return {
                "message": "Post updated successfully",
                "data": data
            }, 200
        else:
            return {
                "message": "Error updating post",
                "data": None,
                "error": "Bad request"
            }, 400
    else:
        return {
            "message": "User not logged in",
            "data": None,
            "error": "Unauthorized"
        }, 401

@new_api.route("/delete_post/<post_id>", methods=["DELETE"])
@token_required
def delete_post(user_id, post_id):
    if user_id is not None:
        if Post.delete_post(post_id):
            return {
                "message": "Post deleted succesfully"
            }, 204
        else:
            return {
                "message": "Error deleting post",
                "data": None,
                "error": "Bad request"
            }, 400
    else:
        return {
            "message": "User not logged in",
            "data": None,
            "error": "Unauthorized"
        }, 401