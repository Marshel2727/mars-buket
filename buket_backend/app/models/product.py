from app import db
import datetime
import uuid

class Kategori(db.Model):
    __tablename__ = 'kategori'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nama_kategori = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Kategori {self.nama_kategori}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nama_kategori': self.nama_kategori,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_kategori = db.Column(db.String(36), db.ForeignKey('kategori.id'), nullable=False)
    nama_produk = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    harga = db.Column(db.Float, nullable=False)
    stok = db.Column(db.Integer, nullable=False)
    gambar_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.nama_produk}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_kategori': self.id_kategori,
            'nama_produk': self.nama_produk,
            'deskripsi': self.deskripsi,
            'harga': self.harga,
            'stok': self.stok,
            'gambar_url': self.gambar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class VarianProduk(db.Model):
    __tablename__ = 'varian_produk'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_produk = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    nama_varian = db.Column(db.String(100), nullable=False)
    harga_varian = db.Column(db.Float, nullable=False)
    stok_varian = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<VarianProduk {self.nama_varian}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_produk': self.id_produk,
            'nama_varian': self.nama_varian,
            'harga_varian': self.harga_varian,
            'stok_varian': self.stok_varian,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class GaleriProduk(db.Model):
    __tablename__ = 'galeri_produk'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_produk = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    url_gambar = db.Column(db.String(255), nullable=False)
    is_utama = db.Column(db.Boolean, default=False) # Menandai apakah gambar ini adalah gambar utama
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<GaleriProduk {self.url_gambar}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_produk': self.id_produk,
            'url_gambar': self.url_gambar,
            'is_utama': self.is_utama,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }