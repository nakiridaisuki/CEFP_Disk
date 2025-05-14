from flask import (
    Blueprint,
    request,
)
import bcrypt
from api.extention import limiter, db
from models import Users
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

        if username is None or password is None:
            return standard_response(
                success=False,
                message="No username or password",
                code=400
            )
        
        user = Users.query.filter_by(name=username).first()
        if not user is None:
            return standard_response(
                success=False,
                message="Username has been used",
                code=403
            )
        
        data = Users(username, password)
        db.session.add(data)
        db.session.commit()
        
        return standard_response(
            data = {
                'name': username
            }
        )
    
    