from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.response import error_response

def role_required(*roles):
    """
    Decorator untuk membatasi akses endpoint hanya untuk peran (role) tertentu.
    Memeriksa klaim 'role' di dalam JWT token.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Validasi keberadaan dan keabsahan token JWT dalam request
            verify_jwt_in_request()
            # Ambil claims tambahan dari JWT payload
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in roles:
                return error_response(
                    message="Akses ditolak. Hak akses tidak mencukupi.",
                    status_code=403
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required():
    """
    Decorator shortcut khusus untuk membatasi akses hanya bagi admin.
    """
    return role_required('admin')
