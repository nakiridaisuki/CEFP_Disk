from flask import (
    Blueprint,
    request,
    send_file
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.extention import limiter
from api.utils import standard_response
from models import Files, Users
from io import BytesIO

download_api = Blueprint('download', __name__)

@download_api.route('/api/file/download', methods=['GET'])
@limiter.limit('100 pre minut')
@jwt_required()
def download():
  """
  Download file
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
      description: Return a file
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
  return send_file(BytesIO(file.file), download_name=file.file_name, as_attachment=True)
  
    