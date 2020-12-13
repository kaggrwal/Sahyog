from flask import Blueprint, make_response, current_app
from flask_login import login_required, current_user
from .. import rpc
from ..schemas.ApiResponse import ApiResponse

main = Blueprint('main', __name__)

@main.route('/')
def index():
    #return "welcome",200
    return ApiResponse(result='welcome, please login',status=200)

@main.route('/profile')
@login_required
def profile():
    current_app.logger.info("Profile action called")
    return ApiResponse(status=200,result="hello "+current_user.user_dict['first_name'])

