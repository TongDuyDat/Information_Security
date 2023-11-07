from flask import Blueprint
from api_control.user_control_api import user_api
from api_control.news_control_api import new_api
from api_control.file_api import api_file

api = Blueprint("api", __name__, url_prefix="/")

api.register_blueprint(user_api)
api.register_blueprint(new_api)
api.register_blueprint(api_file)