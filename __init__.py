import logging
import os
from datetime import timedelta

from flask import Flask, request
from flask_login import LoginManager
from flask_nameko import FlaskPooledClusterRpcProxy
from datetime import datetime as dt


from .models.UserModel import User
from .utils.flask_logs import LogSetup


from .schemas.ApiResponse import ApiResponse

rpc = FlaskPooledClusterRpcProxy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'sahyog-secret'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=10)
    app.config.update(dict(
        NAMEKO_AMQP_URI='amqp://localhost:5672'
    ))
    app.config['MONGODB_URI_KEY'] = 'mongodb://localhost:27017/Sahyog'

    app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "stream")
    app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")

    logs = LogSetup()
    logs.init_app(app)

    rpc.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'main.index'
    login_manager.init_app(app)

#    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
       user =  rpc.user_service.getUserById(user_id)
       print(type(user))
       userLoaded = User(user_dict=user)
       print(userLoaded.user_dict)
       return userLoaded

    # Did I mention we log timestamps in UTC here?
    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
        "%s [%s] %s %s %s %s %s %s",
            request.remote_addr,
            dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.json,
            response.status,
            request.referrer,
            request.user_agent,
        )
        return response


    app.response_class = ApiResponse
    # blueprint for auth routes in our app
    from .resources.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .resources.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

