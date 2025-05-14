from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import jwt_required
from api.extention import db, limiter
from api.utils import standard_response

upload_api = Blueprint('upload', __name__)

@upload_api.route('/api/auth/upload', methods=['POST'])
@limiter.limit('20 pre minut')
@jwt_required()
def upload():
    """
    Upload file
    ---
    tags:
        - 
    parameters:
        - name: username
          in: formData
          type: string
          required: true
        - access_token: jwt token
          in: formData
          type: string
          required: true

        - filename: original file name
          in: fromData
          type: string
          requried: true
        - data: data that uploaded
          in: fromData
          type: 
          requried: true
        - KMS_keyId: KMS key id
          in: fromData
          type: string
          requried: true
        - encrypted_key: encrypted key
          in: fromData
          type: string
          requried: true
        - iv: AES's iv
          in: fromData
          type: string
          requried: true
    response:
        200:
            discription: success uploaded
        400:
            discription: Form data lose
        401:
            discription: Error access token
    """
    if request.method == 'POST':
        # username = request.form.get('name', None)
        # token = request.form.get('access_token', None)
        # users = db.get_all_users()
        
        # if username is None:
        #     return standard_response(
        #         success=False,
        #         message="No username or password",
        #         code=400
        #     )
        
        # if not username in users:
        #     return standard_response(
        #         success=False,
        #         message='User not found',
        #         code=400
        #     )
        
        # user_data = db.get_user_data(username)
        # salt = user_data['salt'].encode('utf-8')
        # hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        # if hashed != user_data['hashed_password']:
        #     return standard_response(
        #         success=False,
        #         message='Error password',
        #         code=401
        #     )
        
        # if not user_data.get('totp_secret', None) is None:
        #     return standard_response(
        #         success=True,
        #         message='Have 2fa',
        #         code=302
        #     )
        
        # token = create_access_token(user_data['id'])
        # user_data['access_token'] = token
        # db.update_user(user_data['id'], user_data)
        
        # return standard_response(data=user_data)

        return standard_response()
    
    