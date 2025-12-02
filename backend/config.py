import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_for_dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "C:/resume_uploads"
    # app/celeryconfig.py (New Naming Convention)
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'
    include = ['app.tasks']
    

