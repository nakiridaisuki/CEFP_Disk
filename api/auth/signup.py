from flask import (
    Blueprint,
    request,
)
import bcrypt
from api.extention import db, limiter
from api.utils import standard_response

signup_api = Blueprint('signup', __name__)

@signup_api.route('/api/auth/signup', methods=['POST'])
@limiter.limit('10 pre hour')
def signup():
    """
    Sign up
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
        403:
            discription: username has been used
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
        
        if username in users:
            return standard_response(
                success=False,
                message="Username has been used",
                code=403
            )
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        user_data = {
            'name': username,
            'hashed_password': hashed.decode('utf-8'),
            'salt': salt.decode('utf-8'),
            'totp_secret': None
        }
        user_data = db.add_user(user_data)
        
        return standard_response(data=user_data)
    
    