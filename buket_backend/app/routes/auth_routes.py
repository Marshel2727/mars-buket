from flask import Blueprint, request
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema
from app.services.auth_service import AuthService

# Sesuaikan nama file utils Anda, misalnya dari app.utils.response
from app.utils.response import success_response, error_response 

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    # 1. Ambil data dari request
    json_data = request.get_json()

    # 2. Validasi input menggunakan Schema
    schema = UserRegisterSchema()
    errors = schema.validate(json_data)
    if errors:
        return error_response(message="Validasi gagal", status_code=400, data=errors)

    # 3. Proses ke Service Layer
    result, status_code = AuthService.register_user(json_data)

    # 4. Kembalikan response sesuai hasil Service
    if status_code == 200 or status_code == 201:
        return success_response(data=result.get('data'), message=result['message'], status_code=status_code)
    else:
        return error_response(message=result['message'], status_code=status_code)


@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()

    # 1. Validasi input
    schema = UserLoginSchema()
    errors = schema.validate(json_data)
    if errors:
        return error_response(message="Validasi gagal", status_code=400, data=errors)

    # 2. Proses ke Service Layer
    result, status_code = AuthService.verify_user(json_data['email'], json_data['password'])

    # 3. Kembalikan response
    if status_code == 200:
        data = {
            "user": result.get('data'),
            "access_token": result.get('access_token')
        }
        return success_response(data=data, message=result['message'])
    else:
        return error_response(message=result['message'], status_code=status_code)