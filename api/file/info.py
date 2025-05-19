from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.extention import limiter
from api.utils import standard_response
from models import Files, Users

fileinfo_api = Blueprint('fileinfo', __name__)

@fileinfo_api.route('/api/file/fileinfo', methods=['GET'])
@limiter.limit('30 pre minut')
@jwt_required()
def fileinfo():
  """
  Get all data's infomation
  ---
  tags:
      - About Files
  produces: application/json,
  security:
    - BearerAuth: []
  responses:
    200:
      description: Return all files' info of this user in a list
      content:
        application/json:
          name: fileName
          size: fileSize
          time: uploadTime
          id: fileId
    400:
      description: User not found
    401:
      description: Error access token
  """

  username = get_jwt_identity()
  
  user: Users = Users.query.filter_by(name=username).first()
  if user is None:
    return standard_response(
      success=False,
      message="User not found",
      code=400
    )
  
  userfiles: list[Files] = user.files
  data = []
  for file in userfiles:
    data.append({
      'name': file.file_name,
      'id': file.id,
      'size': file.file_size,
      'time': file.upload_time
    })
  
  return standard_response(data=data)

  