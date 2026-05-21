from app import db
from app.models.user import User, Address_Book
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register_user(data):
        
        if User.query.filter_by(email=data['email']).first():
            return {
                'status': 'error',
                'message': 'Email sudah terdaftar'
            }, 400
        
        if User.query.filter_by(username=data['username']).first():
            return {
                'status': 'error',
                'message': 'Username sudah terdaftar'
            }, 400
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=User.generate_password_hash(data['password']),
            nomor_telepon=data.get('nomor_telepon'),
            alamat=data.get('alamat')
        )

        db.session.add(new_user)
        try:
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Pendaftaran berhasil',
                'data': new_user.to_dict()
            },200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal mendaftar: {str(e)}'
            }, 500
        

    @staticmethod
    def verify_user(email, password):

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {
                'status': 'error',
                'message': 'Email atau password salah'
            }, 401
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role}
        )

        return {
            'status': 'success',
            'message': 'Login berhasil',
            'data': user.to_dict(),
            'access_token': access_token
        }, 200

class AddressBookService:
    @staticmethod
    def add_address(data, user_id):
        address = Address_Book(
            user_id=user_id,
            nama_kontak=data.get('nama_kontak'),
            nomor_telepon=data.get('nomor_telepon'),
            label_alamat=data.get('label_alamat'),
            nama_penerima=data.get('nama_penerima'),
            alamat_lengkap=data.get('alamat_lengkap')
        )

        db.session.add(address)
        try:
            db.session.commit()
            # RETURN DIPERBAIKI (MENGGUNAKAN TUPLE)
            return {
                'status': 'success',
                'message': 'Alamat berhasil ditambahkan',
                'data': address.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal menambahkan alamat: {str(e)}'
            }, 500

    
    @staticmethod
    def get_addresses(user_id):
        addresses = Address_Book.query.filter_by(user_id=user_id).all()
        # RETURN DIPERBAIKI (MENGGUNAKAN TUPLE DAN LIST COMPREHENSION)
        return {
            'status': 'success',
            'message': 'Data alamat berhasil diambil',
            'data': [addr.to_dict() for addr in addresses]
        }, 200
    
    @staticmethod
    def get_address_by_id(address_id, user_id):
        address = Address_Book.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return {
                'status': 'error',
                'message': 'Alamat tidak ditemukan'
            }, 404
            
        return {
            'status': 'success',
            'message': 'Data alamat berhasil diambil',
            'data': address.to_dict()
        }, 200
        
    @staticmethod
    def update_address(address_id, data, user_id):
        address = Address_Book.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return {
                'status': 'error',
                'message': 'Alamat tidak ditemukan'
            }, 404
        
        address.nama_kontak = data.get('nama_kontak', address.nama_kontak)
        address.nomor_telepon = data.get('nomor_telepon', address.nomor_telepon)
        address.label_alamat = data.get('label_alamat', address.label_alamat)
        address.nama_penerima = data.get('nama_penerima', address.nama_penerima)
        address.alamat_lengkap = data.get('alamat_lengkap', address.alamat_lengkap)

        try:
            db.session.commit()
            # RETURN DIPERBAIKI (MENGGUNAKAN TUPLE)
            return {
                'status': 'success',
                'message': 'Alamat berhasil diperbarui',
                'data': address.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal memperbarui alamat: {str(e)}'
            }, 500

    
    @staticmethod
    def delete_address(address_id, user_id):
        address = Address_Book.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return {
                'status': 'error',
                'message': 'Alamat tidak ditemukan'
            }, 404
        
        db.session.delete(address)
        try:
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Alamat berhasil dihapus'
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f'Gagal menghapus alamat: {str(e)}'
            }, 500