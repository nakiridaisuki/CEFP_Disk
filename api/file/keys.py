from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.extention import limiter, db
from api.utils import standard_response
from models import Files, Users
import base64

keys_api = Blueprint('keys', __name__)

@keys_api.route('/api/file/getkeys', methods=['GET'])
@limiter.limit('30 pre minut')
@jwt_required()
def get_keys():
  """
  Get KMS keyID, iv, encrypted key
  ---
  tags:
      - About Files
  produces: application/json,
  security:
    - BearerAuth: []
  parameters:
  - name: username
    in: formData
    type: string
    required: true
  - name: fileID
    in: formData
    type: integer
    required: true
  responses:
    200:
      description: Return this file's KMS keyID, iv, encrypted key
      content:
        application/json:
          kmsKeyID: KMSkeyid
          iv: 
          encryptedKey: 
    400:
      description: User not found
    401:
      description: Error access token
  """
  username = get_jwt_identity()
  file_id = int(request.args.get('fileID', None))
  
  if username is None or file_id is None:
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
  
  file: Files = Files.query.filter_by(id=file_id).first()
  data = {
    'kmsKeyID': file.key_id,
    'iv': ''.join('{:02x}'.format(x) for x in file.iv),
    'encryptedKey': base64.b64encode(file.encrypted_key).decode('utf-8')
  }
  
  return standard_response(data=data)
  
@keys_api.route('/api/file/updatekeys', methods=['POST'])
@limiter.limit('30 pre minut')
@jwt_required()
def update_keys():
  """
  Update KMS keyID and encrypted key
  ---
  tags:
      - About Files
  produces: application/json,
  security:
    - BearerAuth: []
  parameters:
  - name: username
    in: formData
    type: string
    required: true
  - name: fileID
    in: formData
    type: integer
    required: true
  - name: kmsKeyID
    in: formData
    type: string
    required: true
  - name: encryptedKey
    in: formData
    type: file
    required: true
  responses:
    200:
      description: Update this file's KMS keyID and encrypted key 
    400:
      description: User not found
    401:
      description: Error access token
  """
  if request.method == 'POST':

    username = request.form.get('username', None)
    file_id = request.form.get('fileID', None)
    encrypted_key = request.files['encryptedKey'].read()
    key_id = request.form['kmsKeyID']
    
    if username is None or file_id is None:
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
    
    file: Files = Files.query.filter_by(id=file_id).first()
    file.encrypted_key = encrypted_key
    file.key_id = key_id
    db.session.commit()
    
    return standard_response()