#! /usr/bin/env python
import os

from app import create_app, db, create_blockchain
from app.models import User,Document

app = create_app()

if __name__ == '__main__':
    create_blockchain()
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)

#flask shell command will invoke this function and register items returned by it in the shell session
@app.shell_context_processor
def create_shell_context():
    return {'db': db, 'User': User, 'Document': Document}