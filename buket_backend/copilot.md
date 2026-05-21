# GitHub Copilot Instructions - Backend Development (Flask & SQLAlchemy)
# Project: Web Buket (E-Commerce Bouquet Platform)

You are an expert Software Architect specializing in Python, Flask, Flask-SQLAlchemy, and Flask-Marshmallow. You must strictly follow the directory structure, database rules, and domain-driven model relationships defined below for every code recommendation you generate.

---

## 1. PROJECT DIRECTORY STRUCTURE
Always respect and follow this specific layered project layout when suggesting code locations or references:
- `app/__init__.py`: Application Factory (initializes app, db, jwt, etc.).
- `app/config.py`: Environment configurations (Development, Production).
- `app/extensions.py`: Library instantiations (SQLAlchemy, Marshmallow, JWTManager).
- `app/models/`: Database ORM layer:
  - `user.py` -> Holds User, AddressBook models.
  - `product.py` -> Holds Category, Product, Variant, Gallery models.
  - `transaction.py` -> Holds Order, OrderItem, Payment, Shipping, Promo, Review, Wishlist models.
- `app/schemas/`: Serialization and validation layers (Flask-Marshmallow DTOs).
- `app/routes/`: Controllers and Blueprints (`auth_routes.py`, `product_routes.py`, `order_routes.py`).
- `app/services/`: Core business logic (`auth_service.py`, `order_service.py`, `payment_service.py`).
- `app/utils/`: Shared helper functions (`file_handler.py`, `response.py` for standard JSON responses).

---

## 2. GENERAL DATABASE & CODING RULES
- **Language**: Table names, columns, and relationships must retain the exact naming convention from the schema design (primarily Indonesian names like `pesanan`, `produk`, etc.).
- **Naming Convention**: All database columns and tables must strictly use lowercase `snake_case`. No spaces allowed.
- **Soft Migration Friendly**: Ensure all models map precisely to MySQL types via SQLAlchemy.
- **Security**: NEVER hardcode credentials or secrets. Always fetch configurations via environment variables (`os.getenv()`).
- **Data Safety**: Standardize JSON structures utilizing `app/utils/response.py` for uniform API outputs. Never expose raw database exceptions to the client; wrap operations in try-except blocks and log errors using standard Python `logging`.

---

## 3. DATABASE SCHEMA & SPECIFICATION

You must generate models, schemas, and queries aligning exactly with these four core domains:

### A. Domain Autentikasi & Pengguna (File Target: `app/models/user.py`)

#### Table: `users`
- `id_user` (INT, Primary Key, Auto Increment)
- `nama_lengkap` (VARCHAR(100), Not Null)
- `email` (VARCHAR(100), Unique, Not Null)
- `password` (VARCHAR(255), Not Null) -> Stores hashed password
- `no_telepon` (VARCHAR(20))
- `alamat` (TEXT, Nullable) -> *Legacy default fallback address*
- `role` (ENUM('admin', 'pelanggan'), Default: 'pelanggan')

#### Table: `address_book`
- `id_alamat` (INT, Primary Key, Auto Increment)
- `id_user` (INT, Foreign Key referencing `users.id_user`)
- `label_alamat` (VARCHAR(50)) -> E.g., "Rumah", "Kantor"
- `nama_penerima` (VARCHAR(100))
- `no_telepon` (VARCHAR(20))
- `alamat_lengkap` (TEXT)

---

### B. Domain Katalog Produk (File Target: `app/models/product.py`)

#### Table: `kategori`
- `id_kategori` (INT, Primary Key, Auto Increment)
- `nama_kategori` (VARCHAR(100)) -> E.g., "Buket Bunga", "Buket Uang"

#### Table: `produk`
- `id_produk` (INT, Primary Key, Auto Increment)
- `id_kategori` (INT, Foreign Key referencing `kategori.id_kategori`)
- `nama_produk` (VARCHAR(100))
- `deskripsi` (TEXT)
- `harga_dasar` (INT) -> Base price without variants
- `stok` (INT) -> *Legacy global stock*
- `gambar_produk` (VARCHAR(255)) -> *Legacy main thumbnail path*

#### Table: `varian_produk`
- `id_varian` (INT, Primary Key, Auto Increment)
- `id_produk` (INT, Foreign Key referencing `produk.id_produk`)
- `nama_varian` (VARCHAR(50)) -> E.g., "Ukuran S", "Ukuran L"
- `harga_varian` (INT) -> Specific price overwrite for this variant
- `stok_varian` (INT) -> Inventory dedicated to this variant

#### Table: `galeri_produk`
- `id_galeri` (INT, Primary Key, Auto Increment)
- `id_produk` (INT, Foreign Key referencing `produk.id_produk`)
- `url_gambar` (VARCHAR(255)) -> Path/URL to specific image file
- `is_utama` (BOOLEAN, Default: False) -> Flag identifying primary listing picture

---

### C. Domain Transaksi & Operasional (File Target: `app/models/transaction.py`)

#### Table: `pesanan`
- `id_pesanan` (INT, Primary Key, Auto Increment)
- `id_user` (INT, Foreign Key referencing `users.id_user`)
- `id_alamat` (INT, Foreign Key referencing `address_book.id_alamat`)
- `id_promo` (INT, Foreign Key referencing `promo.id_promo`, Nullable)
- `tanggal_pesan` (DATETIME, Default: Current Timestamp)
- `tanggal_pengiriman` (DATE) -> Customer requested bouquet delivery date
- `pesan_kartu_ucapan` (TEXT, Nullable) -> Custom greeting message text
- `total_harga` (INT) -> Grand total transaction cost
- `status_pesanan` (ENUM('menunggu_pembayaran', 'diproses', 'dikirim', 'selesai', 'dibatalkan'))
- `alamat_pengiriman` (TEXT) -> *Legacy fallback string if id_alamat is missing*

#### Table: `detail_pesanan`
- `id_detail` (INT, Primary Key, Auto Increment)
- `id_pesanan` (INT, Foreign Key referencing `pesanan.id_pesanan`)
- `id_produk` (INT, Foreign Key referencing `produk.id_produk`)
- `id_varian` (INT, Foreign Key referencing `varian_produk.id_varian`, Nullable)
- `jumlah` (INT) -> Quantity purchased
- `harga_satuan` (INT) -> Historical price snapshot at purchase point
- `subtotal` (INT) -> Calculated dynamically as (jumlah * harga_satuan)
- `request_khusus` (TEXT, Nullable) -> Structural or customization notes for assembly

#### Table: `pembayaran`
- `id_pembayaran` (INT, Primary Key, Auto Increment)
- `id_pesanan` (INT, Foreign Key referencing `pesanan.id_pesanan`)
- `id_transaksi_gateway` (VARCHAR(100)) -> External Reference ID from Midtrans/Xendit
- `metode_pembayaran` (VARCHAR(50)) -> E.g., "BCA VA", "QRIS", "Gopay"
- `tanggal_bayar` (DATETIME) -> Actual settlement timestamp
- `jumlah_bayar` (INT) -> Amount credited
- `bukti_transfer` (VARCHAR(255), Nullable) -> *Legacy link for manual verifications*
- `payload_gateway` (JSON) -> Raw diagnostic object from payment provider hook
- `status_pembayaran` (ENUM('pending', 'settlement', 'expire', 'cancel', 'deny'))

#### Table: `pengiriman`
- `id_pengiriman` (INT, Primary Key, Auto Increment)
- `id_pesanan` (INT, Foreign Key referencing `pesanan.id_pesanan`)
- `nama_kurir` (VARCHAR(100)) -> E.g., "JNE", "Kurir Internal"
- `no_resi` (VARCHAR(100), Nullable)
- `biaya_ongkir` (INT)
- `status_pengiriman` (ENUM('dikemas', 'dikirim', 'diterima'))

---

## 4. Domain Marketing & Fitur Pendukung (File Target: `app/models/transaction.py`)

#### Table: `promo`
- `id_promo` (INT, Primary Key, Auto Increment)
- `kode_promo` (VARCHAR(50), Unique)
- `potongan_harga` (INT) -> Discount value amount
- `kuota` (INT) -> Maximum structural system use threshold
- `tanggal_berakhir` (DATE) -> Promotion expiration window target

#### Table: `ulasan`
- `id_ulasan` (INT, Primary Key, Auto Increment)
- `id_user` (INT, Foreign Key referencing `users.id_user`)
- `id_produk` (INT, Foreign Key referencing `produk.id_produk`)
- `rating` (INT) -> Scale limits validation (1-5 Stars)
- `komentar` (TEXT, Nullable)
- `tanggal_ulasan` (DATETIME, Default: Current Timestamp)

#### Table: `wishlist`
- `id_wishlist` (INT, Primary Key, Auto Increment)
- `id_user` (INT, Foreign Key referencing `users.id_user`)
- `id_produk` (INT, Foreign Key referencing `produk.id_produk`)
- `tanggal_ditambahkan` (DATETIME, Default: Current Timestamp)

---

## 5. ORM RELATIONSHIP RULES & BACKREFS
When writing SQLAlchemy structures, maintain strict reciprocal connections and lazy loading strategies:
- `User` has many `AddressBook`, `Pesanan`, `Ulasan`, and `Wishlist`.
- `Kategori` has many `Produk`.
- `Produk` has many `VarianProduk`, `GaleriProduk`, `DetailPesanan`, `Ulasan`, and `Wishlist`.
- `Pesanan` has one `Pembayaran`, one `Pengiriman`, many `DetailPesanan`, and belongs to `User`, `AddressBook`, and `Promo`.

---

## 6. EXAMPLE MODEL CODE FORMAT
When asked to generate models, structure them using this template pattern:
```python
from app.extensions import db
from datetime import datetime

class Kategori(db.Model):
    __tablename__ = 'kategori'
    
    id_kategori = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_kategori = db.Column(db.String(100), nullable=False)
    
    # Relationships
    produk = db.relationship('Produk', backref='kategori', lazy=True)