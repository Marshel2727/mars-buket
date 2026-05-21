from marshmallow import Schema, fields, validate

class KategoriSchema(Schema):
    id = fields.Str(dump_only=True)
    nama_kategori = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=50, error="Nama kategori harus antara 3 hingga 50 karakter"),
        error_messages={"required": "Nama kategori wajib diisi."}
    )

class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    id_kategori = fields.Str(
        required=True, 
        error_messages={"required": "ID Kategori wajib disertakan."}
    )
    nama_produk = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=100, error="Nama produk harus antara 3 hingga 100 karakter"),
        error_messages={"required": "Nama produk wajib diisi."}
    )
    deskripsi = fields.Str(
        validate=validate.Length(max=500, error="Deskripsi tidak boleh melebihi 500 karakter"), 
        allow_none=True
    )
    harga = fields.Float(
        required=True, 
        validate=validate.Range(min=0.01, error="Harga harus lebih besar dari 0"),
        error_messages={"required": "Harga wajib diisi."}
    )
    stok = fields.Int(
        required=True, 
        validate=validate.Range(min=0, error="Stok tidak boleh negatif"),
        error_messages={"required": "Stok wajib diisi."}
    )
    gambar_url = fields.Str(
        validate=validate.Length(max=255, error="URL gambar tidak boleh melebihi 255 karakter"), 
        allow_none=True
    )

class VarianProdukSchema(Schema):
    id = fields.Str(dump_only=True)
    id_produk = fields.Str(
        required=True, 
        error_messages={"required": "ID Produk wajib disertakan."}
    )
    nama_varian = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=100, error="Nama varian harus antara 3 hingga 100 karakter"),
        error_messages={"required": "Nama varian wajib diisi."}
    )
    harga_varian = fields.Float(
        required=True, 
        validate=validate.Range(min=0.01, error="Harga varian harus lebih besar dari 0"),
        error_messages={"required": "Harga varian wajib diisi."}
    )
    stok_varian = fields.Int(
        required=True, 
        validate=validate.Range(min=0, error="Stok varian tidak boleh negatif"),
        error_messages={"required": "Stok varian wajib diisi."}
    )

class GambarProdukSchema(Schema):
    id = fields.Str(dump_only=True)
    id_produk = fields.Str(
        required=True, 
        error_messages={"required": "ID Produk wajib disertakan."}
    )
    url_gambar = fields.Str(
        required=True, 
        validate=validate.Length(max=255, error="URL gambar tidak boleh melebihi 255 karakter"),
        error_messages={"required": "URL Gambar wajib disertakan."}
    )
    is_utama = fields.Bool(dump_default=False)
