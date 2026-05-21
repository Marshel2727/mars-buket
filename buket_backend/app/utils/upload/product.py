import os
import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/uploads/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_product_image(img_file):
    if not img_file or img_file.filename == '':
        raise ValueError("File is required.")

    if img_file and allowed_file(img_file.filename):
        filename = secure_filename(img_file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        img_file.save(file_path)
        return f"/uploads/products/{unique_filename}"
    else:
        raise ValueError("Invalid file type. Allowed types are: png, jpg, jpeg, gif.")

def delete_product_image(image_url):
    if image_url:
        filename = os.path.basename(image_url)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            