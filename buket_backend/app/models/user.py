from app import db
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False) # Ganti ke nama_lengkap jika ingin ikut PDF
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Diperpanjang ke 255 untuk keamanan hash
    nomor_telepon = db.Column(db.String(20), nullable=True)
    alamat = db.Column(db.Text, nullable=True) # Mengikuti PDF (TEXT)
    role = db.Column(db.String(20), default='pelanggan')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # --- TAMBAHAN METHOD UNTUK PASSWORD HASHING ---
    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nomor_telepon': self.nomor_telepon,
            'alamat': self.alamat,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Address_Book(db.Model):
    __tablename__ = 'address_book'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    nama_kontak = db.Column(db.String(80), nullable=False)
    label_alamat = db.Column(db.String(50), nullable=True)
    nama_penerima = db.Column(db.String(100), nullable=True)
    nomor_telepon = db.Column(db.String(20), nullable=True) 
    alamat_lengkap = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<AddressBook {self.nama_kontak}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nama_kontak': self.nama_kontak,
            'label_alamat': self.label_alamat,
            'nama_penerima': self.nama_penerima,
            'nomor_telepon': self.nomor_telepon,
            'alamat_lengkap': self.alamat_lengkap,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }