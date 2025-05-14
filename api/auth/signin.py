from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import create_access_token
import bcrypt
from api.extention import db, limiter
from api.utils import standard_response

signin_api = Blueprint('signin', __name__)

@signin_api.route('/api/auth/signin', methods=['POST'])
@limiter.limit('5 pre minut')
def signin():
    """
    Sign in
    ---
    tags:
        - 
    parameters:
        - name: username
          in: formData
          type: string
          required: true
        - password: password
          in: formData
          type: string
          required: true
    response:
        200:
            discription: success singed up
            content:
                application/json:
                    name: username
                    totp_secret: null
                    access_token: token

        400:
            discription: User not found
        401:
            discription: Error password
    """
    if request.method == 'POST':
        username = request.form.get('name', None)
        password = request.form.get('password', None)
        users = db.get_all_users()
        
        if username is None or password is None:
            return standard_response(
                success=False,
                message="No username or password",
                code=400
            )
        
        if not username in users:
            return standard_response(
                success=False,
                message='User not found',
                code=400
            )
        
        user_data = db.get_user_data(username)
        salt = user_data['salt'].encode('utf-8')
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        if hashed != user_data['hashed_password']:
            return standard_response(
                success=False,
                message='Error password',
                code=401
            )
        
        if not user_data.get('totp_secret', None) is None:
            return standard_response(
                success=True,
                message='Have 2fa',
                code=302
            )
        
        token = create_access_token(user_data['id'])
        user_data['access_token'] = token
        db.update_user(user_data['id'], user_data)
        
        return standard_response(data=user_data)
    
    