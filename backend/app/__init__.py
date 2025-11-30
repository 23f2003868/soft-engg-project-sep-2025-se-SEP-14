from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery
from flask_login import LoginManager
import redis
from flask_cors import CORS
from flasgger import Swagger
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
from flask_cors import CORS
def make_celery(app):
    app.config['UPLOAD_FOLDER'] = 'C:\\documents_mad2'
    # Celery Configuration (Updated to new format)
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERY_INCLUDE'] = ['app.tasks']  # Corrected format for including tasks
    login_manager.init_app(app)  # Initialize the login manager
    # Initialize Celery
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


    from app.routes import main
    app.register_blueprint(main)

    app.celery = make_celery(app)

    return app

