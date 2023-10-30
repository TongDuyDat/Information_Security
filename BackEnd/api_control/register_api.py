from flask import Blueprint
from api_control.user_control_api import user_api


api = Blueprint("api", __name__, url_prefix="/")

api.register_blueprint(user_api)