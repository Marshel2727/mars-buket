from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.order_schema import PesananCheckoutSchema
from app.services.order_service import OrderService
from app.utils.response import success_response, error_response
from app.utils.security import role_required

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/v1/orders')

# ==========================================
# 1. ENDPOINT CHECKOUT (BUAT PESANAN)
# ==========================================
@order_bp.route('/checkout', methods=['POST'])
@role_required('admin', 'pelanggan')
def checkout():
    current_user_id = get_jwt_identity()
    json_data = request.get_json()

    # Validasi input data checkout menggunakan Schema
    schema = PesananCheckoutSchema()
    errors = schema.validate(json_data)
    if errors:
        return error_response(message="Validasi gagal", status_code=400, data=errors)

    # Proses pembuatan pesanan di Service Layer
    result, status_code = OrderService.checkout(json_data, current_user_id)

    if status_code == 201:
        return success_response(data=result.get('data'), message=result['message'], status_code=status_code)
    else:
        return error_response(message=result['message'], status_code=status_code)


# ==========================================
# 2. ENDPOINT RIWAYAT PESANAN USER
# ==========================================
@order_bp.route('/', methods=['GET'])
@role_required('admin', 'pelanggan')
def get_my_orders():
    current_user_id = get_jwt_identity()
    
    # Ambil seluruh daftar pesanan milik user yang sedang login
    result, status_code = OrderService.get_user_orders(current_user_id)
    
    if status_code == 200:
        return success_response(data=result.get('data'), message=result['message'], status_code=status_code)
    else:
        return error_response(message=result['message'], status_code=status_code)


# ==========================================
# 3. ENDPOINT DETAIL TRANSAKSI SPESIFIK
# ==========================================
@order_bp.route('/<string:order_id>', methods=['GET'])
@role_required('admin', 'pelanggan')
def get_order_by_id(order_id):
    current_user_id = get_jwt_identity()
    
    # Ambil detail pesanan dan rincian item di dalamnya berdasarkan ID Pesanan (UUID)
    result, status_code = OrderService.get_order_detail(order_id, current_user_id)
    
    if status_code == 200:
        return success_response(data=result.get('data'), message=result['message'], status_code=status_code)
    else:
        return error_response(message=result['message'], status_code=status_code)