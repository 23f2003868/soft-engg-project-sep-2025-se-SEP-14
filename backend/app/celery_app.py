from celery import Celery
from app import create_app

# Create flask app
flask_app = create_app()

# Expose celery instance to command line
celery = flask_app.celery