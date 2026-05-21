import os
import time
from urllib.parse import quote_plus
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def db_uri():
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '3306')
    name = os.getenv('DB_NAME', 'mars_portfol')

    return f'mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{name}'

class Config():
    SQLALCHEMY_DATABASE_URI = db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'rahasia-super-aman-portofolio-mars')

#untuk mengecek apakah data base sudah terkoneksi
def db_connection():
    uri = Config.SQLALCHEMY_DATABASE_URI
    retries = int(os.getenv('DB_CONNECT_RETRIES', '10'))
    delay = int(os.getenv('DB_CONNECT_DELAY', '3'))

    for attempt in range(1, retries + 1):
        try:
            engine = create_engine(uri, pool_pre_ping=True)
            with engine.connect():
                print('database berhasil terkoneksi')
            return engine
        except OperationalError as e:
            if attempt == retries:
                raise RuntimeError(f'Database gagal terkoneksi setelah {retries} percobaan: {e}') from e
            print(f'Database belum siap, mencoba lagi ({attempt}/{retries})...')
            time.sleep(delay)
