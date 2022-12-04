from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_app(app):
    db.app = app
    db.init_app(app)


class User(db.Model):


    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    feedback = db.relationship('Feedback', backref='user', cascade='delete')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hash = bcrypt.generate_password_hash(password).decode('utf8')
        return cls(username=username, password=hash, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))

