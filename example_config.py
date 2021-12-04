"""
Settings of the core Flask app
"""
from datetime import timedelta
import os


class Config:
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = 'development'
    SECRET_KEY = 'c3qxpmrdm4vhuylf768d121hds12'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
    DATASET_CONTAINER = '/home/mebaysan/workspace/datasets'
    WH_CONFIG = {
        'SERVER': '10.0.0.1',
        'USER': 'db_username',
        'PASSWORD': 'db_password',
        'DATABASE': 'db_name'
    }
