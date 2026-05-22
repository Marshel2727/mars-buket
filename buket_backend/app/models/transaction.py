from app import db
import datetime
import uuid

class Pesanan(db.Model):
    __tablename__ = 'pesanan'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    id_alamat = db.Column(db.String(36), db.ForeignKey('address_book.id'), nullable=True) # Mengikuti PDF, opsional/fallback
    id_promo = db.Column(db.String(36), nullable=True) # Sementara dikosongkan, diisi UUID promo nanti jika ada
    tanggal_pesan = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    tanggal_pengiriman = db.Column(db.Date, nullable=False)
    pesan_kartu_ucapan = db.Column(db.Text, nullable=True)
    total_harga = db.Column(db.Float, nullable=False)
    status_pesanan = db.Column(db.String(50), default='menunggu_pembayaran') # ENUM: menunggu_pembayaran, diproses, dikirim, selesai, dibatalkan
    alamat_pengiriman = db.Column(db.Text, nullable=True) # Fallback jika id_alamat kosong

    def __repr__(self):
        return f'<Pesanan {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_user': self.id_user,
            'id_alamat': self.id_alamat,
            'id_promo': self.id_promo,
            'tanggal_pesan': self.tanggal_pesan.isoformat() if self.tanggal_pesan else None,
            'tanggal_pengiriman': self.tanggal_pengiriman.isoformat() if self.tanggal_pengiriman else None,
            'pesan_kartu_ucapan': self.pesan_kartu_ucapan,
            'total_harga': self.total_harga,
            'status_pesanan': self.status_pesanan,
            'alamat_pengiriman': self.alamat_pengiriman
        }

class DetailPesanan(db.Model):
    __tablename__ = 'detail_pesanan'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_pesanan = db.Column(db.String(36), db.ForeignKey('pesanan.id'), nullable=False)
    id_produk = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    id_varian = db.Column(db.String(36), db.ForeignKey('varian_produk.id'), nullable=True) # Opsional, jika tanpa varian
    jumlah = db.Column(db.Integer, nullable=False)
    harga_satuan = db.Column(db.Float, nullable=False) # Snapshot harga saat transaksi
    subtotal = db.Column(db.Float, nullable=False) # jumlah x harga_satuan
    request_khusus = db.Column(db.Text, nullable=True) # Catatan untuk perakit buket

    def __repr__(self):
        return f'<DetailPesanan {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_pesanan': self.id_pesanan,
            'id_produk': self.id_produk,
            'id_varian': self.id_varian,
            'jumlah': self.jumlah,
            'harga_satuan': self.harga_satuan,
            'subtotal': self.subtotal,
            'request_khusus': self.request_khusus
        }

class Pembayaran(db.Model):
    __tablename__ = 'pembayaran'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_pesanan = db.Column(db.String(36), db.ForeignKey('pesanan.id'), nullable=False)
    id_transaksi_gateway = db.Column(db.String(100), nullable=True) # ID dari Midtrans/Xendit
    metode_pembayaran = db.Column(db.String(50), nullable=True) # Cth: "BCA VA", "QRIS"
    tanggal_bayar = db.Column(db.DateTime, nullable=True)
    jumlah_bayar = db.Column(db.Float, nullable=False)
    bukti_transfer = db.Column(db.String(255), nullable=True) # Fallback manual transfer
    payload_gateway = db.Column(db.JSON, nullable=True) # Log raw data dari webhook gateway
    status_pembayaran = db.Column(db.String(50), default='pending') # ENUM: pending, settlement, expire, cancel, deny

    def __repr__(self):
        return f'<Pembayaran {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_pesanan': self.id_pesanan,
            'id_transaksi_gateway': self.id_transaksi_gateway,
            'metode_pembayaran': self.metode_pembayaran,
            'tanggal_bayar': self.tanggal_bayar.isoformat() if self.tanggal_bayar else None,
            'jumlah_bayar': self.jumlah_bayar,
            'bukti_transfer': self.bukti_transfer,
            'payload_gateway': self.payload_gateway,
            'status_pembayaran': self.status_pembayaran
        }

class Pengiriman(db.Model):
    __tablename__ = 'pengiriman'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_pesanan = db.Column(db.String(36), db.ForeignKey('pesanan.id'), nullable=False)
    nama_kurir = db.Column(db.String(100), nullable=True) # Cth: "JNE", "Kurir Internal"
    no_resi = db.Column(db.String(100), nullable=True)
    biaya_ongkir = db.Column(db.Float, default=0.0)
    status_pengiriman = db.Column(db.String(50), default='dikemas') # ENUM: dikemas, dikirim, diterima

    def __repr__(self):
        return f'<Pengiriman {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_pesanan': self.id_pesanan,
            'nama_kurir': self.nama_kurir,
            'no_resi': self.no_resi,
            'biaya_ongkir': self.biaya_ongkir,
            'status_pengiriman': self.status_pengiriman
        }