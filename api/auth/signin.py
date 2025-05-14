from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import create_access_token
from api.extention import db, limiter
from api.utils import standard_response
from models import Users

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
                    access_token: token

        400:
            discription: User not found
        401:
            discription: Error password
    """
    if request.method == 'POST':
        username = request.form.get('name', None)
        password = request.form.get('password', None)
        
        if username is None or password is None:
            return standard_response(
                success=False,
                message="No username or password",
                code=400
            )
        
        user: Users = Users.query.filter_by(name=username).first()
        if user is None:
            return standard_response(
                success=False,
                message="User not found",
                code=400
            )

        if not user.verify_password(password) :
            return standard_response(
                success=False,
                message='Error password',
                code=401
            )
        
        if not user.totp_secret is None:
            return standard_response(
                success=True,
                message='Have 2fa',
                code=302
            )
        
        token = create_access_token(user.id)
        
        return standard_response(
            data = {
                'name': username,
                'access_token': token
            }
        )
    
    