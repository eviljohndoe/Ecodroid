import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG')
    APP_EXTENSIONS = os.environ.get('APP_EXTENSIONS')
    IMAGE_EXTENSIONS = os.environ.get('IMAGE_EXTENSIONS').split()
    ADB = os.path.join(basedir, 'platform-tools/adb')
    PROJECT_FOLDER = os.path.join(basedir, 'app/static/projects')
