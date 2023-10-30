
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson import ObjectId
from flask import Blueprint
from upload import test
from api_control.register_api import api
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
    jwt = JWTManager(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)