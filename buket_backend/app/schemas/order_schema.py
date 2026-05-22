from marshmallow import Schema, fields, validate

class DetailPesananInputSchema(Schema):
    # Validasi untuk setiap item buket yang dibeli di dalam keranjang
    id_produk = fields.Str(
        required=True, 
        error_messages={"required": "ID Produk wajib disertakan pada item."}
    )
    id_varian = fields.Str(allow_none=True)
    jumlah = fields.Int(
        required=True, 
        validate=validate.Range(min=1, error="Jumlah pembelian minimal 1 pcs."),
        error_messages={"required": "Jumlah barang wajib diisi."}
    )
    request_khusus = fields.Str(
        validate=validate.Length(max=500, error="Catatan request terlalu panjang."), 
        allow_none=True
    )

class PesananCheckoutSchema(Schema):
    # Validasi utama saat user menekan tombol "Checkout / Buat Pesanan"
    id_alamat = fields.Str(allow_none=True)
    alamat_pengiriman = fields.Str(
        validate=validate.Length(max=500), 
        allow_none=True
    ) # Fallback manual jika tidak memilih dari address book
    
    tanggal_pengiriman = fields.Date(
        required=True, 
        error_messages={"required": "Tanggal permintaan pengiriman wajib diisi."}
    )
    pesan_kartu_ucapan = fields.Str(
        validate=validate.Length(max=1000, error="Pesan kartu ucapan maksimal 1000 karakter."), 
        allow_none=True
    )
    id_promo = fields.Str(allow_none=True)
    
    # Menampung list/daftar item keranjang belanja menggunakan nested schema di atas
    items = fields.List(
        fields.Nested(DetailPesananInputSchema), 
        required=True, 
        validate=validate.Length(min=1, error="Keranjang belanja tidak boleh kosong."),
        error_messages={"required": "Daftar item pesanan wajib disertakan."}
    )

class UpdateStatusPesananSchema(Schema):
    # Digunakan oleh Admin untuk memperbarui status pengerjaan buket
    status_pesanan = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['menunggu_pembayaran', 'diproses', 'dikirim', 'selesai', 'dibatalkan'],
            error="Status pesanan tidak valid."
        )
    )

class InputResiPengirimanSchema(Schema):
    # Digunakan oleh Admin saat buket diserahkan ke kurir
    nama_kurir = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "Nama kurir wajib diisi."}
    )
    no_resi = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=100),
        error_messages={"required": "Nomor resi wajib diisi."}
    )
    biaya_ongkir = fields.Float(
        validate=validate.Range(min=0), 
        load_default=0.0
    )