# Library App

## REST API Flask application.

+ DB migration
+ Blueprints
+ Errors
+ Logs
+ Docker

### Installation (/library)
+ (venv) pip install -r requirements.txt
+ flask db upgrade

### Run
+ flask run


### Docker:
+ docker build -t library:latest .
+ docker run -it -p 8000:5000 library:latest
