from flask import (
    Blueprint,
    request,
)
import pyotp
import qrcode
import io
import base64
from flask_jwt_extended import create_access_token
from api.extention import db
from api.utils import standard_response
from models import Users


twofa_api = Blueprint('twofa', __name__)

@twofa_api.route('/api/auth/twofa/setup', methods=['POST'])
def twofa_setup():
    """
    Setup 2FA
    ---
    tags:
        - 
    parameters:
        - name: username
          in: fromData
          type: string
          required: true
        - reset: if need reset secret key
          in: fromData
          type: bool
          required: false
          default: false
    response:
        200:
            discription: success setup
            content:
                application/json:
                    qrcode: img
                    totp_secret: null
        400:
            discription: User not found
    """
    if request.method == 'POST':
        username = request.form.get('name', None)
        reset = request.form.get('reset', False)

        if username is None:
            return standard_response(
                success=False,
                message='No username',
                code=400
            )

        user: Users = Users.query.filter_by(name=username).first()
        if user is None:
            return standard_response(
                success=False,
                message="User not found",
                code=400
            )
        
        totp_secret = user.totp_secret

        if reset or totp_secret is None:
            totp_secret = pyotp.random_base32()
            user.tmp_totp_secret = totp_secret
            user.totp_secret = None
            db.session.commit()

        auth_url = pyotp.totp.TOTP(totp_secret).provisioning_uri(
            name=username,
            issuer_name='Secure app'
        )
        img = qrcode.make(auth_url)
        buf = io.BytesIO()
        img.save(buf)
        img_data = base64.b64encode(buf.getvalue()).decode('ascii')
        return standard_response(
            data = {
                'qrcode': img_data,
                'totp_secret': totp_secret
            }
        )

@twofa_api.route('/api/auth/twofa/verify', methods=['POST'])
def twofa_verify():
    """
    Verify 2FA
    ---
    tags:
        - 
    parameters:
        - name: username
          in: fromData
          type: string
          required: true
        - code: 2fa code
          in: fromData
          type: str
          required: true
    response:
        200:
            discription: success verified
            content:
                application/json:
                    access_token: token
        400:
            discription: code not corect
    """
    if request.method == 'POST':
        username = request.form.get('name', None)
        code = request.form.get('code', None)

        if username is None or code is None:
            return standard_response(
                success=False,
                message='No username or code',
                code=400
            )
        
        user: Users = Users.query.filter_by(name=username).first()
        if user is None:
            return standard_response(
                success=False,
                message="User not found",
                code=400
            )

        if not user.tmp_totp_secret is None:
            first_check = True
            totp_secret = user.tmp_totp_secret
        else:
            first_check = False
            totp_secret = user.totp_secret

        if pyotp.TOTP(totp_secret).verify(code, valid_window=1):
            token = create_access_token(user.id)
            if first_check:
                user.totp_secret = totp_secret
                user.tmp_totp_secret = None
                db.session.commit()

            return standard_response(
                data = {
                    'access_token': token
                }
            )
        else:
            return standard_response(
                success=False,
                message='Error otp code',
                code=400
            )


        