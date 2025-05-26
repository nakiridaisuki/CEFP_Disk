from api.extention import db

user_files = db.Table('user_files',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('file_id', db.Integer, db.ForeignKey('files.id'), primary_key=True)
)


from .file import Files
from .user import Users