from marshmallow import Schema, fields, validate

class UserAddressSchema(Schema):
    nama_kontak = fields.Str(required=True, validate=validate.Length(min=3, max=80, error="Nama kontak harus antara 3 hingga 80 karakter"))
    nomor_telepon = fields.Str(required=True, validate=validate.Length(max=20, error="Nomor telepon tidak boleh melebihi 20 karakter"))
    label_alamat = fields.Str(required=True, validate=validate.Length(max=50, error="Label alamat tidak boleh melebihi 50 karakter")    )
    nama_penerima = fields.Str(required=True, validate=validate.Length(min=3, max=80, error="Nama penerima harus antara 3 hingga 80 karakter"))
    alamat_lengkap = fields.Str(required=True, validate=validate.Length(min=10, max=200, error="Alamat lengkap harus antara 10 hingga 200 karakter"))