from flask import Flask
from flask_cors import CORS
from config import DATABASE_URL, JWT_SECRET_KEY, TEMPLATE_FOLDER, STATIC_FOLDER

from models import  Users, Files

def create_app(mode: str = None) -> Flask:
    app = Flask('app',
                static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER)

    CORS(app)

    from api.extention import db
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()

    if mode == 'testing':
        db.drop_all()
    db.create_all()

    from api.extention import jwt
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    jwt.init_app(app)

    if mode is None:
        from api.extention import limiter
        limiter.init_app(app)


    from .auth.signup import signup_api
    app.register_blueprint(signup_api)

    from .auth.signin import signin_api
    app.register_blueprint(signin_api)

    from .auth.two_factor import twofa_api
    app.register_blueprint(twofa_api)

    from .file.upload import upload_api
    app.register_blueprint(upload_api)

    from .file.info import info_api
    app.register_blueprint(info_api)

    from .file.download import download_api
    app.register_blueprint(download_api)

    from .file.keys import keys_api
    app.register_blueprint(keys_api)

    from .file.delete import delete_api
    app.register_blueprint(delete_api)

    from .file.update import update_api
    app.register_blueprint(update_api)

    return app