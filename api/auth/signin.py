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
    - Sign in/up
  produces: application/json,
  parameters:
  - name: username
    in: formData
    type: string
    required: true
  - name: password
    in: formData
    type: string
    required: true
  responses:
    200:
      description: Success singed up
      content:
        application/json:
          name: username
          accessToken: token
    302:
      description: Need 2FA code
    400:
      description: User not found
    401:
      description: Error password
  """
  if request.method == 'POST':
    username = request.form.get('username', None)
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
    
    token = create_access_token(user.name)
    
    return standard_response(
      data = {
        'name': username,
        'accessToken': token
    }
  )

  