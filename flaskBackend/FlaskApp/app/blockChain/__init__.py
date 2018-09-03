from flask import Blueprint

bp = Blueprint('blockChain', __name__)

from app.blockChain import routes

