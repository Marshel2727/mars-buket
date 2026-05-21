from app import db
# Pastikan memuat GaleriProduk dari model Anda
from app.models.product import Product, Kategori, VarianProduk, GaleriProduk 

# === KategoriService, ProductService, dan VarianProdukService milik Anda sudah bagus ===
class KategoriService:
    @staticmethod
    def create_kategori(data):
        try:
            new_kategori = Kategori(nama_kategori=data['nama_kategori'])
            db.session.add(new_kategori)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Kategori berhasil dibuat',
                'data': new_kategori.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal membuat kategori: {str(e)}'
            }, 500
    
    @staticmethod
    def get_all_kategori():
        try:
            kategoris = Kategori.query.all()
            return {
                'status': 'success',
                'message': 'Kategori berhasil diambil',
                'data': [kategori.to_dict() for kategori in kategoris]
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil kategori: {str(e)}'
            }, 500
    
    @staticmethod
    def get_kategori_by_id(kategori_id):
        try:
            kategori = Kategori.query.get(kategori_id)
            if not kategori:
                return {
                    'status': 'error',
                    'message': 'Kategori tidak ditemukan'
                }, 404
            return {
                'status': 'success',
                'message': 'Kategori berhasil diambil',
                'data': kategori.to_dict()
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil kategori: {str(e)}'
            }, 500
    
    @staticmethod
    def update_kategori(kategori_id, data):
        try:
            kategori = Kategori.query.get(kategori_id)
            if not kategori:
                return {
                    'status': 'error',
                    'message': 'Kategori tidak ditemukan'
                }, 404
            kategori.nama_kategori = data['nama_kategori']
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Kategori berhasil diperbarui',
                'data': kategori.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal memperbarui kategori: {str(e)}'
            }, 500
    
    @staticmethod
    def delete_kategori(kategori_id):
        try:
            kategori = Kategori.query.get(kategori_id)
            if not kategori:
                return {
                    'status': 'error',
                    'message': 'Kategori tidak ditemukan'
                }, 404
            db.session.delete(kategori)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Kategori berhasil dihapus'
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal menghapus kategori: {str(e)}'
            }, 500

class ProductService:
    @staticmethod
    def create_product(data):
        try:
            new_product = Product(
                id_kategori=data['id_kategori'],
                nama_produk=data['nama_produk'],
                deskripsi=data.get('deskripsi'),
                harga=data['harga'],
                stok=data['stok'],
                gambar_url=data.get('gambar_url')
            )
            db.session.add(new_product)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Produk berhasil dibuat',
                'data': new_product.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal membuat produk: {str(e)}'
            }, 500
    
    @staticmethod
    def get_all_products():
        try:
            products = Product.query.all()
            return {
                'status': 'success',
                'message': 'Produk berhasil diambil',
                'data': [product.to_dict() for product in products]
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil produk: {str(e)}'
            }, 500
    
    @staticmethod
    def get_product_by_id(product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }, 404
            return {
                'status': 'success',
                'message': 'Produk berhasil diambil',
                'data': product.to_dict()
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil produk: {str(e)}'
            }, 500

    @staticmethod
    def update_product(product_id, data):
        try:
            product = Product.query.get(product_id)
            if not product:
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }, 404
            product.id_kategori = data['id_kategori']
            product.nama_produk = data['nama_produk']
            product.deskripsi = data.get('deskripsi')
            product.harga = data['harga']
            product.stok = data['stok']
            product.gambar_url = data.get('gambar_url')
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Produk berhasil diperbarui',
                'data': product.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal memperbarui produk: {str(e)}'
            }, 500
    
    @staticmethod
    def delete_product(product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }, 404
            db.session.delete(product)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Produk berhasil dihapus'
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal menghapus produk: {str(e)}'
            }, 500

class VarianProdukService:
    @staticmethod
    def create_varian_produk(data):
        try:
            new_varian = VarianProduk(
                id_produk=data['id_produk'],
                nama_varian=data['nama_varian'],
                harga_varian=data['harga_varian'],
                stok_varian=data['stok_varian']
            )
            db.session.add(new_varian)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Varian produk berhasil dibuat',
                'data': new_varian.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal membuat varian produk: {str(e)}'
            }, 500
    
    @staticmethod
    def get_varian_by_produk_id(product_id):
        try:
            varians = VarianProduk.query.filter_by(id_produk=product_id).all()
            return {
                'status': 'success',
                'message': 'Varian produk berhasil diambil',
                'data': [varian.to_dict() for varian in varians]
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil varian produk: {str(e)}'
            }, 500
            
    @staticmethod
    def get_varian_by_id(varian_id):
        try:
            varian = VarianProduk.query.get(varian_id)
            if not varian:
                return {
                    'status': 'error',
                    'message': 'Varian produk tidak ditemukan'
                }, 404
            return {
                'status': 'success',
                'message': 'Varian produk berhasil diambil',
                'data': varian.to_dict()
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil varian produk: {str(e)}'
            }, 500
    
    @staticmethod
    def delete_varian(varian_id):
        try:
            varian = VarianProduk.query.get(varian_id)
            if not varian:
                return {
                    'status': 'error',
                    'message': 'Varian produk tidak ditemukan'
                }, 404
            db.session.delete(varian)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Varian produk berhasil dihapus'
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal menghapus varian produk: {str(e)}'
            }, 500
    
    @staticmethod
    def update_varian(varian_id, data):
        try:
            varian = VarianProduk.query.get(varian_id)
            if not varian:
                return {
                    'status': 'error',
                    'message': 'Varian produk tidak ditemukan'
                }, 404
            varian.nama_varian = data['nama_varian']
            varian.harga_varian = data['harga_varian']
            varian.stok_varian = data['stok_varian']
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Varian produk berhasil diperbarui',
                'data': varian.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal memperbarui varian produk: {str(e)}'
            }, 500

# === SEKTOR REVISI UTAMA: GambarProdukService disesuaikan ke model GaleriProduk ===
class GambarProdukService:
    @staticmethod
    def add_gambar_produk(product_id, gambar_url, is_utama=False):
        try:
            # Pastikan produknya ada dulu sebelum diberi gambar galeri
            product = Product.query.get(product_id)
            if not product:
                return {
                    'status': 'error',
                    'message': 'Produk tidak ditemukan'
                }, 404
            
            # Jika diset sebagai gambar utama, matikan gambar utama lama milik produk ini
            if is_utama:
                GaleriProduk.query.filter_by(id_produk=product_id).update({GaleriProduk.is_utama: False})

            new_gallery = GaleriProduk(
                id_produk=product_id,
                url_gambar=gambar_url,
                is_utama=is_utama
            )
            db.session.add(new_gallery)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Gambar berhasil ditambahkan ke galeri produk',
                'data': new_gallery.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal menambahkan gambar produk: {str(e)}'
            }, 500
            
    @staticmethod
    def get_gallery_by_product_id(product_id):
        try:
            # Ambil semua record gambar yang tersambung dengan id_produk dari tabel galeri_produk
            gallery_items = GaleriProduk.query.filter_by(id_produk=product_id).all()
            return {
                'status': 'success',
                'message': 'Gambar galeri produk berhasil diambil',
                'data': [item.to_dict() for item in gallery_items]
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil gambar produk: {str(e)}'
            }, 500
            
    @staticmethod
    def get_gambar_by_id(image_id):
        try:
            image_item = GaleriProduk.query.get(image_id)
            if not image_item:
                return {
                    'status': 'error',
                    'message': 'Gambar galeri tidak ditemukan'
                }, 404
            return {
                'status': 'success',
                'message': 'Gambar galeri berhasil diambil',
                'data': image_item.to_dict()
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal mengambil gambar galeri: {str(e)}'
            }, 500
        
    @staticmethod
    def delete_gambar_produk(image_id):
        try:
            # Mencari record spesifik berdasarkan id gambar di tabel galeri_produk
            image_item = GaleriProduk.query.get(image_id)
            if not image_item:
                return {
                    'status': 'error',
                    'message': 'Gambar galeri tidak ditemukan'
                }, 404
            
            db.session.delete(image_item)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Gambar galeri produk berhasil dihapus'
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal menghapus gambar produk: {str(e)}'
            }, 500