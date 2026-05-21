from flask import Blueprint, request
from app.services.product_service import (
    KategoriService,
    ProductService,
    VarianProdukService,
    GambarProdukService
)
from app.utils.upload.product import save_product_image, delete_product_image
from app.schemas.product_schema import KategoriSchema, ProductSchema, VarianProdukSchema, GambarProdukSchema
from app.utils.response import success_response, error_response

product_bp = Blueprint('product_bp', __name__, url_prefix='/api/v1')

def handle_service_response(result, status_code):
    if status_code >= 400:
        return error_response(result.get('message', 'Error'), status_code, result.get('data'))
    return success_response(result.get('data'), result.get('message', 'Success'), status_code)

# ==========================================
# 1. ENDPOINTS KATEGORI
# ==========================================

@product_bp.route('/kategori', methods=['POST'])
def create_kategori():
    try:
        data = request.get_json()
        schema = KategoriSchema()
        validated_data = schema.load(data)
        result, status_code = KategoriService.create_kategori(validated_data)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 400)

@product_bp.route('/kategori', methods=['GET'])
def get_all_kategori():
    try:
        result, status_code = KategoriService.get_all_kategori()
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

@product_bp.route('/kategori/<string:kategori_id>', methods=['GET'])
def get_kategori(kategori_id):
    try:
        result, status_code = KategoriService.get_kategori_by_id(kategori_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

@product_bp.route('/kategori/<string:kategori_id>', methods=['PUT'])
def update_kategori(kategori_id):
    try:
        data = request.get_json()
        schema = KategoriSchema()
        validated_data = schema.load(data)
        result, status_code = KategoriService.update_kategori(kategori_id, validated_data)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 400)

@product_bp.route('/kategori/<string:kategori_id>', methods=['DELETE'])
def delete_kategori(kategori_id):
    try:
        result, status_code = KategoriService.delete_kategori(kategori_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)
    
# ==========================================
# 2. ENDPOINTS PRODUK   
# ==========================================

@product_bp.route('/produk', methods=['POST'])
def create_produk():
    try:
        data = request.form.to_dict()
        schema = ProductSchema()
        validated_data = schema.load(data)
        
        if 'gambar' in request.files:
            file = request.files['gambar']
            gambar_url = save_product_image(file)
            validated_data['gambar_url'] = gambar_url
        
        result, status_code = ProductService.create_product(validated_data)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 400)
    
@product_bp.route('/produk', methods=['GET'])
def get_all_produk():
    try:
        result, status_code = ProductService.get_all_products()
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

@product_bp.route('/produk/<string:produk_id>', methods=['GET'])
def get_produk(produk_id):
    try:
        result, status_code = ProductService.get_product_by_id(produk_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

@product_bp.route('/produk/<string:produk_id>', methods=['PUT'])
def update_produk(produk_id):
    try:
        data = request.form.to_dict()
        schema = ProductSchema()
        validated_data = schema.load(data)
        
        if 'gambar' in request.files:
            file = request.files['gambar']
            gambar_url = save_product_image(file)
            validated_data['gambar_url'] = gambar_url
            
            # Hapus gambar lama jika ada
            existing, code = ProductService.get_product_by_id(produk_id)
            if code == 200 and existing.get('data') and existing['data'].get('gambar_url'):
                delete_product_image(existing['data']['gambar_url'])
        
        result, status_code = ProductService.update_product(produk_id, validated_data)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 400)

@product_bp.route('/produk/<string:produk_id>', methods=['DELETE'])
def delete_produk(produk_id):
    try:
        # Hapus gambar produk jika ada
        existing, code = ProductService.get_product_by_id(produk_id)
        if code == 200 and existing.get('data') and existing['data'].get('gambar_url'):
            delete_product_image(existing['data']['gambar_url'])
        
        result, status_code = ProductService.delete_product(produk_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)
    
# ==========================================
# 3. ENDPOINTS VARIAN PRODUK
# ==========================================
@product_bp.route('/varian', methods=['POST'])
def create_varian():
    try:
        data = request.get_json()
        schema = VarianProdukSchema()
        validated_data = schema.load(data)
        result, status_code = VarianProdukService.create_varian_produk(validated_data)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 400)

@product_bp.route('/produk/<string:produk_id>/varian', methods=['GET'])
def get_varian_by_produk(produk_id):
    try:
        result, status_code = VarianProdukService.get_varian_by_produk_id(produk_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

@product_bp.route('/varian/<string:varian_id>', methods=['GET'])
def get_varian(varian_id):
    try:
        result, status_code = VarianProdukService.get_varian_by_id(varian_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

@product_bp.route('/varian/<string:varian_id>', methods=['PUT'])
def update_varian(varian_id):
    try:
        data = request.get_json()
        schema = VarianProdukSchema()
        validated_data = schema.load(data)
        result, status_code = VarianProdukService.update_varian(varian_id, validated_data)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 400)

@product_bp.route('/varian/<string:varian_id>', methods=['DELETE'])
def delete_varian(varian_id):
    try:
        result, status_code = VarianProdukService.delete_varian(varian_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

#=========================================
# 4. ENDPOINTS GAMBAR PRODUK
#=========================================

@product_bp.route('/produk/<string:produk_id>/gallery', methods=['POST'])
def upload_gambar_produk(produk_id):
    try:
        if 'gambar' not in request.files:
            return error_response("File gambar tidak ditemukan dalam request.", 400)
        
        file = request.files['gambar']
        gambar_url = save_product_image(file)
        
        # Mendukung parameter is_utama dari form data jika diperlukan
        is_utama = request.form.get('is_utama', 'false').lower() == 'true'

        result, status_code = GambarProdukService.add_gambar_produk(produk_id, gambar_url, is_utama)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 400)

@product_bp.route('/produk/<string:produk_id>/gallery/<string:gambar_id>', methods=['DELETE'])
def delete_gambar_produk(produk_id, gambar_id):
    try:
        existing, code = GambarProdukService.get_gambar_by_id(gambar_id)
        if code == 200 and existing.get('data') and existing['data'].get('url_gambar'):
            delete_product_image(existing['data']['url_gambar'])
            
        result, status_code = GambarProdukService.delete_gambar_produk(gambar_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)

@product_bp.route('/produk/<string:produk_id>/gallery', methods=['GET'])
def get_gambar_produk(produk_id):
    try:
        result, status_code = GambarProdukService.get_gallery_by_product_id(produk_id)
        return handle_service_response(result, status_code)
    except Exception as e:
        return error_response(str(e), 500)
