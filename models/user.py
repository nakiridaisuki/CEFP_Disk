from api.extention import db
import bcrypt

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    totp_secret = db.Column(db.String(100), nullable=True)
    tmp_totp_secret = db.Column(db.String(100), nullable=True)

    files = db.relationship('Files', backref='user')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, password):
        salt = bcrypt.gensalt()
        self.salt = salt
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password):
        salt = self.salt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return self.password_hash == password_hash