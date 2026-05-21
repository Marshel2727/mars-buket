from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=100, error="Username harus antara 3 hingga 100 karakter"))
    
    email = fields.Email(
        required=True, 
        validate=validate.Length(min=3, max=120),
        error_messages={"invalid": "Format email tidak valid", "required": "Email wajib diisi"})
    
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=6, error="Password harus setidaknya 6 karakter"))
    
    nomor_telepon = fields.Str(
        validate=validate.Length(max=20, error="Nomor telepon tidak boleh melebihi 20 karakter"))
    alamat = fields.Str()

    role = fields.Str(
        validate=validate.OneOf(['admin', 'pelanggan'], error="Role harus salah satu dari: admin, pelanggan"))

class UserLoginSchema(Schema):
    email = fields.Email(
        required=True, 
        validate=validate.Length(min=3, max=120, error="Email harus antara 3 hingga 120 karakter"))
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=6, error="Password harus setidaknya 6 karakter"))

class GambarProdukSchema(Schema):
    id_produk = fields.Str(
        required=True, 
        error_messages={"required": "ID Produk wajib disertakan."}
    )
    gambar_url = fields.Str(
        required=True, 
        validate=validate.Length(max=255, error="URL gambar tidak boleh melebihi 255 karakter"),
        error_messages={"required": "URL gambar wajib diisi."}
    )