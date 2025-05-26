from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import jwt_required
from api.extention import db, limiter
from api.utils import standard_response
from models import Files, Users

upload_api = Blueprint('upload', __name__)

@upload_api.route('/api/file/upload', methods=['POST'])
@limiter.limit('30 pre minut')
@jwt_required()
def upload():
  """
  Upload file
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

  - name: filename
    in: formData
    type: string
    required: true
  - name: kmsKeyID
    in: formData
    type: string
    required: true
  - name: encryptedData
    in: formData
    type: file
    required: true
  - name: encryptedKey
    in: formData
    type: file
    required: true
  - name: iv
    in: formData
    type: file
    required: true
  responses:
    200:
      description: success uploaded
    400:
      description: Form data lose
    401:
      description: Error access token
  """
  if request.method == 'POST':

    username = request.form.get('username', None)

    try:
      encrypted_data = request.files['encryptedFile'].read()
      encrypted_key = request.files['encryptedKey'].read()
      iv = request.files['iv'].read()
      file_name = request.form.get('filename', 'unknowfile')
      key_id = request.form['kmsKeyID']
    except KeyError as e:
      return standard_response(
        success=False,
        message="Lose some datas",
        code=400
      )
    
    if username is None:
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

    
    file = Files(file_name, key_id, encrypted_key, iv, encrypted_data, user.name)
    user.files.append(file)
    db.session.add(file)
    db.session.commit()
    
    return standard_response()
  
    