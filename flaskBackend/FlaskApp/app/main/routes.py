#from datetime import datetime
from flask import render_template, request, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from flask import send_file
from datetime import datetime
from app.models import User
from app.blockChain import BlockChain
from app.document import Document
from app.users import Groups


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        #current_user.last_online = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Dashboard')