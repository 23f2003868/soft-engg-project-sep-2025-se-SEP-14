from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from celery import Celery
import redis

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# Celery Setup
def make_celery(app: Flask):
    celery = Celery(
        app.import_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
        include=['app.tasks']
    )

    celery.conf.update(app.config)

    class FlaskContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = FlaskContextTask
    return celery


# Flask Factory
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True
    )


    from app.routes import main
    app.register_blueprint(main)

    # Initialize Celery
    app.celery = make_celery(app)

    return app
