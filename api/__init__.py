from flask import Flask
from config import DATABASE_URL, JWT_SECRET_KEY


def create_app(mode: str = None) -> Flask:
    app = Flask(__name__)

    from api.extention import db
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    import modelref
    db.init_app(app)
    app.app_context().push()
    # db.drop_all()
    db.create_all()

    from api.extention import jwt
    jwt.init_app(app)
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

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

    return app