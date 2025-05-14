from flask import Flask
from database import get_db
from config import DATABASE_PATH, TEST_DATABASE_PATH, JWT_SECRET_KEY


def create_app(mode: str = None) -> Flask:
    app = Flask(__name__)
    if mode == 'testing':
        get_db(TEST_DATABASE_PATH)
    else:
        get_db(DATABASE_PATH)

    from api.extention import jwt
    jwt.init_app(app)
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

    from .auth.signup import signup_api
    app.register_blueprint(signup_api)

    from .auth.signin import signin_api
    app.register_blueprint(signin_api)

    return app