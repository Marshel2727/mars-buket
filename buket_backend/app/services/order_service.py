from app import db
from app.models.transaction import Pesanan, DetailPesanan, Pembayaran, Pengiriman
from app.models.product import Product, VarianProduk
from app.models.user import Address_Book
import datetime

class OrderService:
    @staticmethod
    def checkout(data, user_id):
        try:
            # 1. Validasi Input Dasar
            items = data.get('items')
            if not items or not isinstance(items, list):
                return {'status': 'error', 'message': 'Keranjang belanja kosong atau format tidak valid.'}, 400
            tanggal_pengiriman = data.get('tanggal_pengiriman')
            if not tanggal_pengiriman:
                return {'status': 'error', 'message': 'Tanggal pengiriman wajib diisi.'}, 400
            
            if isinstance(tanggal_pengiriman, str):
                try:
                    tanggal_pengiriman = datetime.datetime.strptime(tanggal_pengiriman, "%Y-%m-%d").date()
                except ValueError:
                    return {'status': 'error', 'message': 'Format tanggal_pengiriman harus YYYY-MM-DD.'}, 400

            # 2. Validasi Alamat Pengiriman
            alamat_final = data.get('alamat_pengiriman')
            if data.get('id_alamat'):
                addr_book = Address_Book.query.filter_by(id=data['id_alamat'], user_id=user_id).first()
                if not addr_book:
                    return {'status': 'error', 'message': 'Alamat book tidak ditemukan.'}, 404
                alamat_final = addr_book.alamat_lengkap
            if not alamat_final:
                return {'status': 'error', 'message': 'Alamat pengiriman wajib ditentukan.'}, 400
            # Inisialisasi hitungan harga
            total_harga = 0.0
            detail_items_to_save = []
            
            # 3. Validasi & Pemotongan Stok Langsung (Loop Keranjang Belanja)
            for item in items:
                jumlah_item = item.get('jumlah', 1) # Default 1 jika tidak diset
                if jumlah_item <= 0:
                    return {'status': 'error', 'message': 'Jumlah produk harus lebih dari 0.'}, 400
                
                prod = Product.query.filter_by(id=item.get('id_produk')).first()
                if not prod:
                    return {'status': 'error', 'message': f"Produk dengan ID {item.get('id_produk')} tidak ditemukan."}, 404
                harga_satuan = prod.harga
                varian_obj = None
                # Jika item menggunakan varian spesifik
                if item.get('id_varian'):
                    varian_obj = VarianProduk.query.filter_by(id=item['id_varian'], id_produk=prod.id).first()
                    if not varian_obj:
                        return {'status': 'error', 'message': f"Varian tidak cocok dengan produk {prod.nama_produk}."}, 400
                    
                    # Validasi dan potong stok dari varian (langsung ubah state objeknya)
                    if varian_obj.stok_varian < jumlah_item:
                        return {'status': 'error', 'message': f"Stok varian '{varian_obj.nama_varian}' tidak mencukupi."}, 400
                    
                    varian_obj.stok_varian -= jumlah_item # Potong stok varian langsung
                    harga_satuan = varian_obj.harga_varian
                else:
                    # Validasi dan potong stok dari produk utama (langsung ubah state objeknya)
                    if prod.stok < jumlah_item:
                        return {'status': 'error', 'message': f"Stok produk '{prod.nama_produk}' tidak mencukupi."}, 400
                    
                    prod.stok -= jumlah_item # Potong stok utama langsung
                # Hitung subtotal item
                subtotal_item = harga_satuan * jumlah_item
                total_harga += subtotal_item
                # Tampung data detail pesanan sementara ke memori
                detail_items_to_save.append({
                    'id_produk': prod.id,
                    'id_varian': item.get('id_varian'),
                    'jumlah': jumlah_item,
                    'harga_satuan': harga_satuan,
                    'subtotal': subtotal_item,
                    'request_khusus': item.get('request_khusus')
                    
                })
            # 4. Mulai Simpan ke Database (ACID Transaction)
            new_order = Pesanan(
                id_user=user_id,
                id_alamat=data.get('id_alamat'),
                id_promo=data.get('id_promo'),
                tanggal_pengiriman=tanggal_pengiriman,
                pesan_kartu_ucapan=data.get('pesan_kartu_ucapan'),
                total_harga=total_harga,
                alamat_pengiriman=alamat_final,
                status_pesanan='menunggu_pembayaran'
            )
            db.session.add(new_order)
            db.session.flush() # Ambil ID Pesanan sebelum commit permanen
            # Simpan Detail Item
            for detail in detail_items_to_save:
                order_detail = DetailPesanan(
                    id_pesanan=new_order.id,
                    id_produk=detail['id_produk'],
                    id_varian=detail['id_varian'],
                    jumlah=detail['jumlah'],
                    harga_satuan=detail['harga_satuan'],
                    subtotal=detail['subtotal'],
                    request_khusus=detail['request_khusus']
                )
                db.session.add(order_detail)
            # Buat record Pembayaran awal (Pending)
            new_payment = Pembayaran(
                id_pesanan=new_order.id,
                jumlah_bayar=total_harga,
                status_pembayaran='pending'
            )
            db.session.add(new_payment)
            # Buat record Pengiriman awal (Dikemas)
            new_shipping = Pengiriman(
                id_pesanan=new_order.id,
                status_pengiriman='dikemas'
            )
            db.session.add(new_shipping)
            # Commit semua operasi (termasuk pengurangan stok dan record pesanan baru)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Pesanan berhasil dibuat, silakan lakukan pembayaran.',
                'data': new_order.to_dict()
            }, 201  # BUG FIX: diubah dari 21 menjadi 201
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Transaksi gagal diproses: {str(e)}'
            }, 500

    @staticmethod
    def get_user_orders(user_id):
        try:
            orders = Pesanan.query.filter_by(id_user=user_id).order_by(Pesanan.tanggal_pesan.desc()).all()
            return {
                'status': 'success',
                'message': 'Riwayat pesanan berhasil diambil',
                'data': [order.to_dict() for order in orders]
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': f'Gagal mengambil data: {str(e)}'}, 500

    @staticmethod
    def get_order_detail(order_id, user_id):
        try:
            order = Pesanan.query.filter_by(id=order_id, id_user=user_id).first()
            if not order:
                return {'status': 'error', 'message': 'Pesanan tidak ditemukan.'}, 404

            details = DetailPesanan.query.filter_by(id_pesanan=order.id).all()
            
            payload = order.to_dict()
            payload['items'] = [item.to_dict() for item in details]
            
            return {
                'status': 'success',
                'message': 'Detail transaksi berhasil ditemukan',
                'data': payload
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': f'Gagal memproses data: {str(e)}'}, 500