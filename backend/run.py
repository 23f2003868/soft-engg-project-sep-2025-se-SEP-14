from app import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)


# celery -A celery_worker.celery worker --loglevel=info --pool=solo