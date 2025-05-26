from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.extention import limiter, db
from api.utils import standard_response
from models import Files, Users

update_api = Blueprint('update', __name__)

@update_api.route('/api/file/update-owner', methods=['POST'])
@limiter.limit('30 pre minut')
@jwt_required()
def update_keys():
  """
  Update KMS keyID, encrypted key and owners
  ---
  tags:
      - About Files
  produces: application/json,
  security:
    - BearerAuth: []
  parameters:
  - name: fileId
    in: formData
    type: integer
    required: true
  - name: kmsKeyId
    in: formData
    type: string
    required: true
  - name: encryptedKey
    in: formData
    type: file
    required: true
  - name: allowedUsers
    in: formData
    type: list
    requeird: true
  responses:
    200:
      description: Update this file's KMS keyID and encrypted key 
    400:
      description: User not found
    401:
      description: Error access token
  """
  if request.method == 'POST':

    try:
      username = get_jwt_identity()
      file_id = request.form['fileId']
      encrypted_key = request.files['encryptedKey'].read()
      key_id = request.form['kmsKeyId']
      allowed_users = request.form['allowedUsers']
    except:
      return standard_response(
        success=False,
        message="Lose some data",
        code=400
      )
    
    allowed_users = allowed_users.split(',')
    
    user: Users = Users.query.filter_by(name=username).first()
    if user is None:
      return standard_response(
        success=False,
        message="User not found",
        code=400
      )
    
    file: Files = Files.query.filter_by(id=file_id).first()

    if file.owner_name != username:
      return standard_response(
        success=False,
        message="permission denied",
        code=401
      )

    file.encrypted_key = encrypted_key
    file.key_id = key_id
    file.user = Users.query.filter(Users.name.in_(allowed_users)).all()

    db.session.commit()
    
    return standard_response()