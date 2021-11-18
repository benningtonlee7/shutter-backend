from flask import Flask
from application.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from oauthlib.oauth2 import WebApplicationClient
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os



#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db, compare_type=True)
login = LoginManager(app)
login.login_view = "google.login"
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)

from application.resources.ProfileRecourse import Profile
from application import routes, errors

######################################
#### Application Factory Function ####
######################################

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    initialize_extensions(app)
    register_blueprints(app)
    return app


##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (application)
    db.init_app(app)
    login.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    # Flask-Login configuration
    from application.resources.ProfileRecourse import Profile

    @login.user_loader
    def load_profile(id):
        return Profile.query.get(int(id)).first()


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (application)
    from application.oauth import google_blueprint
    app.register_blueprint(google_blueprint, url_prefix="/login")



#
# if not application.debug:
#     if application.config['MAIL_SERVER']:
#         auth = None
#         if application.config['MAIL_USERNAME'] or application.config['MAIL_PASSWORD']:
#             auth = (application.config['MAIL_USERNAME'], application.config['MAIL_PASSWORD'])
#         secure = None
#         if application.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(application.config['MAIL_SERVER'], application.config['MAIL_PORT']),
#             fromaddr='no-reply@' + application.config['MAIL_SERVER'],
#             toaddrs=application.config['ADMINS'], subject='Shutter Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         application.logger.addHandler(mail_handler)
#
#         if not os.path.exists('logs'):
#             os.mkdir('logs')
#         file_handler = RotatingFileHandler('logs/shutter.log', maxBytes=10240,
#                                            backupCount=10)
#         file_handler.setFormatter(logging.Formatter(
#             '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#         file_handler.setLevel(logging.INFO)
#         application.logger.addHandler(file_handler)
#
#         application.logger.setLevel(logging.INFO)
#         application.logger.info('Shutter startup')


