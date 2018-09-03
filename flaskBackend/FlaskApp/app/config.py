"""
Desc: Class for configuration settings
> e.g SECRET_KEY configuration variable > cryptographic key, useful to generate
signatures or tokens
> contains classes for configuration (functioning via inheritance)
"""
import os

#app root - this defines the server path where files are stored
basedir = os.path.abspath(os.path.dirname(__file__))
#file management
ALLOWED_EXTENSIONS = set(['txt', 'json', 'PNG'])
UPLOAD_FOLDER = 'app/uploads'
BLOCK_ROOT = basedir + "/../"
APP_ROOT = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

'''class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    # to allow unit testing forms
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "localhost"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)'''
