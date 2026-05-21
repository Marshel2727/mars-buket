from app import db
from app.services.auth_service import AddressBookService # Pastikan nama classnya sesuai (AddressBookService atau AddressService)
from app.schemas.address_schema import UserAddressSchema
from flask import Blueprint, request
from app.utils.response import success_response, error_response
from flask_jwt_extended import jwt_required, get_jwt_identity

address_bp = Blueprint('address_bp', __name__, url_prefix='/api/v1/addresses')

@address_bp.route('/', methods=['POST'])
@jwt_required()
def add_address():
    current_user_id = get_jwt_identity() # Typo diperbaiki
    json_data = request.get_json()
    schema = UserAddressSchema()
    errors = schema.validate(json_data)
    if errors:
        return error_response(message="Validasi gagal", status_code=400, data=errors)
    
    # Pastikan urutan parameter sesuai dengan fungsi di Service Anda
    result, status_code = AddressBookService.add_address(json_data, current_user_id) 

    if status_code == 200 or status_code == 201:
        return success_response(data=result.get('data'), message=result['message'], status_code=status_code)
    else:
        return error_response(message=result['message'], status_code=status_code)
    
@address_bp.route('/', methods=['GET'])
@jwt_required()
def get_addresses():
    current_user_id = get_jwt_identity()
    result, status_code = AddressBookService.get_addresses(current_user_id)

    if status_code == 200:
        return success_response(data=result.get('data'), message=result['message'])
    else:
        return error_response(message=result['message'], status_code=status_code)
    
# UBAH int MENJADI string KARENA ID MENGGUNAKAN UUID
@address_bp.route('/<string:address_id>', methods=['GET'])
@jwt_required()
def get_address_by_id(address_id):
    current_user_id = get_jwt_identity()
    result, status_code = AddressBookService.get_address_by_id(address_id, current_user_id)

    if status_code == 200:
        return success_response(data=result.get('data'), message=result['message'])
    else:
        return error_response(message=result['message'], status_code=status_code)
    
# UBAH int MENJADI string
@address_bp.route('/<string:address_id>', methods=['PUT'])
@jwt_required()
def update_address(address_id):
    current_user_id = get_jwt_identity()
    json_data = request.get_json()
    schema = UserAddressSchema()
    errors = schema.validate(json_data)
    if errors:
        return error_response(message="Validasi gagal", status_code=400, data=errors)
    
    result, status_code = AddressBookService.update_address(address_id, json_data, current_user_id)

    if status_code == 200:
        return success_response(data=result.get('data'), message=result['message'])
    else:
        return error_response(message=result['message'], status_code=status_code)

# UBAH int MENJADI string
@address_bp.route('/<string:address_id>', methods=['DELETE'])
@jwt_required()
def delete_address(address_id):
    current_user_id = get_jwt_identity()
    result, status_code = AddressBookService.delete_address(address_id, current_user_id)

    if status_code == 200:
        return success_response(message=result['message'])
    else:
        return error_response(message=result['message'], status_code=status_code)