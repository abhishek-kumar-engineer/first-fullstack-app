# routes/profile_routes.py

from flask import Blueprint
from controllers.profile_controller import get_my_profile, update_my_profile, upload_avatar
from middleware.crypto_middleware import decrypt_request, encrypt_response

profile_bp = Blueprint('profile', __name__, url_prefix='/api/auth')

# GET profile — JSON response, encryption applies normally
profile_bp.route('/profile', methods=['GET'])(
    encrypt_response(get_my_profile)
)

# PUT profile — JSON body aata hai, dono encrypt/decrypt lagenge
profile_bp.route('/profile', methods=['PUT'])(
    encrypt_response(decrypt_request(update_my_profile))
)

# POST avatar — multipart/form-data, crypto middleware SKIP
# response JSON hai toh usko encrypt kar sakte hain, lekin request decrypt NAHI
profile_bp.route('/profile/avatar', methods=['POST'])(
    encrypt_response(upload_avatar)
)