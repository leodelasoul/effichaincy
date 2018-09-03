"""
Desc: database model
"""

from datetime import datetime
from app import db, login
#password hashing and verification
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    about_me = db.Column(db.String(140))
    last_online = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(20))
    surname = db.Column(db.String(40))
    status = db.Column(db.String(50))

    @property
    def set_password(self):
        raise AttributeError('password: write-only field')

    @set_password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


groups = db.Table('groups',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
                  )

'''group_to_group = db.Table('group_to_group',
                          db.Column('parent_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
                          db.Column('child_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
                          )'''


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', secondary=groups, backref=db.backref('groups', lazy='dynamic', order_by=name))
    '''parents = db.relationship('Group', secondary=group_to_group, primaryjoin=id == group_to_group.c.parent_id,
                              secondaryjoin=id == group_to_group.c.child_id,
                              backref="children",
                              remote_side=[group_to_group.c.parent_id])'''

    def __repr__(self):
        return self.name
