from datetime import timedelta

from flask import Blueprint, url_for, request, flash, session, current_app
from flask_login import login_user, login_required, logout_user
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash
from varname import nameof
from werkzeug.utils import redirect

from ..models.UserModel import User
from ..exceptions.UserServiceExceptions import UserNotFoundException
from ..exceptions.GeneralErrors import GeneralErrors
from ..exceptions.GeneralExceptions import ValidationFailException, UserServiceException
from ..schemas.UserSchema import UserSchema
from ..schemas.ApiResponse import ApiResponse
from ..exceptions.AuthenticationErrors import AuthenticationErrors
from .. import rpc
import traceback


auth = Blueprint('auth', __name__)
userSchema = UserSchema()


@auth.route('/login', methods=['POST'])
def login_post():
    # request parsing as json
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    current_app.logger.info("Login action called")

    try:
          user = rpc.user_service.getUserByEmailAndPassword(email,password)
          current_app.logger.info("user fetched from UserService: ",user)
          userLoaded = User(user_dict=user)
          #print(userLoaded.user_dict)
          if user:
             login_user(userLoaded, remember=remember)
             session.permanent = True
          else:
               return ApiResponse(result=AuthenticationErrors.LoginFailureError.get('message'),
                         status=AuthenticationErrors.LoginFailureError.get('status'),
                        error=nameof(AuthenticationErrors.LoginFailureError))

            # return redirect(url_for('auth.signup'))

    except UserNotFoundException:
              return ApiResponse(result=AuthenticationErrors.UserNotFoundError.get('message'),
                       status=AuthenticationErrors.UserNotFoundError.get('status'),
                         error=nameof(AuthenticationErrors.UserNotFoundError))
    except UserServiceException as ex:
         return ApiResponse(result=GeneralErrors.InternalServerError.get('message'+ex.msg),
                               status=GeneralErrors.InternalServerError.get('status'),
                               error=ex.errors)
    except Exception as ex:
            return returnErrorResponse(ex)

    return ApiResponse(status=200, result="You have been logged in")


@auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        user,errors = userSchema.load(request.get_json())
        if errors:
            raise (ValidationFailException(errors,"Validation Failed"))

        user = rpc.user_service.getUserByEmail(user['email'])

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            return ApiResponse(result=AuthenticationErrors.UserAlreadyExistsError.get('message'),
                               status=AuthenticationErrors.UserAlreadyExistsError.get('status'),
                               error=nameof(AuthenticationErrors.UserAlreadyExistsError))
            # return redirect(url_for('auth.signup'))

    except UserNotFoundException:
                try:
                    print(user)
                    rpc.user_service.createUser(user)
                except Exception as ex:
                     return returnErrorResponse(ex)

    except ValidationFailException as ex:
                        return ApiResponse(result=GeneralErrors.ValidationError.get('message'),
                               status=GeneralErrors.ValidationError.get('status'),
                               error=ex.errors)
    except UserServiceException as ex:
         return ApiResponse(result=GeneralErrors.InternalServerError.get('message'+ex.msg),
                               status=GeneralErrors.InternalServerError.get('status'),
                               error=ex.errors)

    except Exception as ex:
            return returnErrorResponse(ex)

    return ApiResponse(status=200, result="Your account is created now")
    # return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return ApiResponse(status=200, result="You have been logged out")

def returnErrorResponse(ex):
     traceback.print_exc()
     return ApiResponse(result=GeneralErrors.InternalServerError.get('message'),
                               status=GeneralErrors.InternalServerError.get('status'),
                               error=str(ex))
