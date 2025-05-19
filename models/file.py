from api.extention import db
from datetime import datetime

class Files(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)
    key_id = db.Column(db.String(80), nullable=False)
    upload_time = db.Column(db.String(100), nullable=True)

    iv = db.Column(db.BLOB, nullable=False)
    encrypted_key = db.Column(db.BLOB, nullable=False)
    file = db.Column(db.BLOB, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, filename, keyid, encryptedkey, iv, file, userid):
        self.file_name = filename
        self.key_id = keyid
        self.encrypted_key = encryptedkey
        self.iv = iv
        self.file = file
        self.upload_time = datetime.utcnow().isoformat(timespec='seconds')
        self.file_size = len(file)
        self.user_id = userid