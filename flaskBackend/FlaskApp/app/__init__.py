"""
Desc: Creates application object as an instance of class Flask imported from
Python script at top-level that defines the Flask application instance
"""
import json
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from app.config import Config, ALLOWED_EXTENSIONS,BLOCK_ROOT


#from config import config_by_name

# database stuff
db = SQLAlchemy()
migrate = Migrate()
# authentication configuration
login = LoginManager()
login.session_protection = "strong"
login.login_view = "auth.login"

bootstrap = Bootstrap()
# for displaying timestamps
moment = Moment()

def create_blockchain():
    if not os.path.isfile(os.path.join(BLOCK_ROOT,"blockChain1.json")):
        genesis = BlockChain.BlockChain([])
        dummy_doc = Document.Document("", "")

        genesis.create_genesis(genesis.chain, dummy_doc)

    blockchain_root = os.path.join(BLOCK_ROOT, "blockChain1.json")

    with open(blockchain_root ,"r") as block_init:
        parsed_json = json.load(block_init)
        chain = BlockChain.BlockChain(parsed_json)
        block_init.close()
    #dummy_doc = Document.Document("app/document/Effichaincy/documents/5/lol.txt","")
    #chain.make_version_index(chain.chain,dummy_doc.name)

def create_app():
    '''starting point when Flask needs to load associated resources
    most Flask extenstions are initialised by creating an instance of the extension
    and passing the application as an argument'''
    app = Flask(__name__)
    #app.config.from_object(config_by_name[config_name])
    app.config.from_object(Config)


    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS



    # initialise all app functionalities, passing flask app as argument
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # prefix optional - any routes defined in BP receive prefix in URL
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')


    from app.document import bp as document_bp
    app.register_blueprint(document_bp, url_prefix='/doc')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/user')

    return app



from app import models
from app.blockChain import BlockChain
from app.document import Document