from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.extention import limiter, db
from api.utils import standard_response
from models import Files, Users

delete_api = Blueprint('delete', __name__)

@delete_api.route('/api/file/delete', methods=['GET'])
@limiter.limit('100 pre minut')
@jwt_required()
def download():
  """
  Dlelete file
  ---
  tags:
      - About Files
  produces: application/json,
  security:
    - BearerAuth: []
  parameters:
  - name: fileID
    in: query
    type: integer
    required: true
  responses:
    200:
      description: Success delete
    400:
      description: User not found
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
  
  try:
    file: Files = Files.query.filter_by(id=file_id).first()
    db.session.delete(file)
    db.session.commit()
    return standard_response()
  except:
    return standard_response(success=False, code=500)
  
  
    