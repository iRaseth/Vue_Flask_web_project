from app import db, login, ma
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='post_author', lazy='dynamic')
    privateMessage = db.relationship('PrivateMessage', backref='pm_author', lazy='dynamic')

    def __repr__(self):
        return '<User: {} | password: {}.>'.format(self.username, self.password_hash)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.String(128), db.ForeignKey('user.username'))

    def __repr__(self):
        return '[{},{}]'.format(self.author, self.body)

class PrivateChat(db.Model):
    __tablename__ = 'privatechat'
    id = db.Column(db.Integer, primary_key=True)
    privateMessage = db.relationship('PrivateMessage', backref='dm_author', lazy='dynamic')

    def __repr__(self):
        return '<Private Chat id:  `{}`, author : {}>'.format(self.id)

class PrivateMessage(db.Model):
    __tablename__ = 'privatemessage'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat = db.Column(db.Integer, db.ForeignKey('privatechat.id'))

    def __repr__(self):
        return '<Post `{}`, author : {}>'.format(self.body, self.author)

class SimpleNeuronModel(db.Model):
    __tablename__ = 'simpleneuronmodel'
    id = db.Column(db.Integer, primary_key = True)
    x1 = db.Column(db.Integer)
    x2 = db.Column(db.Integer)
    iterator = db.Column(db.Integer)
    learning_parameter = db.Column(db.Integer)
    expected_output = db.Column(db.Integer)

    def __repr__(self):
        return '[{}, {}, {}, {}, {}]'.format(self.x1, self.x2, self.iterator, self.learning_parameter, self.expected_output)

"""User schema for data serialization"""

class PostSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'author', 'body')

class SimpleNeuronSchema(ma.Schema):
    class Meta:
        #Field to be exposed
        fields = ('x1', 'x2', 'iterator', 'learning_parameter', 'expected_output')

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
