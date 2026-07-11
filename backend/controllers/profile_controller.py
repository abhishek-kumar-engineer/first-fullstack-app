# controllers/profile_controller.py

from flask import request, jsonify
from models.user_model import UserModel
# from models.user_model import get_profile_by_id, update_profile, update_avatar_url
from controllers.auth_controller import token_required  # existing decorator reuse
from utils.response_handler import ResponseHandler       # aapka existing pattern
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@token_required
def get_my_profile(current_user_id):
    """
    GET /api/auth/profile
    token_required decorator se current_user_id already mil jata hai
    (aapke existing pattern jaisa hi — JWT se decode hota hai)
    """
    profile = UserModel.get_profile_by_id(current_user_id)

    if not profile:
        return ResponseHandler.not_found("User not found")

    return ResponseHandler.success(data=profile, message="Profile fetched")


@token_required
def update_my_profile(current_user_id):
    """
    PUT /api/auth/profile
    Body: { "name": "...", "bio": "...", "phone": "..." }
    """
    data = request.get_json()

    if not data:
        return ResponseHandler.validation_error("No data provided")

    name = data.get('name')
    bio = data.get('bio')
    phone = data.get('phone')

    # Basic validation — length checks
    if bio and len(bio) > 500:
        return ResponseHandler.validation_error("Bio must be under 500 characters")
    if phone and len(phone) > 20:
        return ResponseHandler.validation_error("Invalid phone number")

    success = UserModel.update_profile(current_user_id, name=name, bio=bio, phone=phone)

    if not success:
        return ResponseHandler.validation_error("Nothing to update")

    updated_profile = UserModel.get_profile_by_id(current_user_id)
    return ResponseHandler.success(data=updated_profile, message="Profile updated")


@token_required
def upload_avatar(current_user_id):
    """
    POST /api/auth/profile/avatar
    multipart/form-data — NOTE: ye crypto_middleware se encrypted NAHI hoga
    (JSON encryption sirf application/json body ke liye hai)
    """
    if 'avatar' not in request.files:
        return ResponseHandler.validation_error("No file uploaded")

    file = request.files['avatar']

    if file.filename == '':
        return ResponseHandler.validation_error("No file selected")

    if not allowed_file(file.filename):
        return ResponseHandler.validation_error("Only png, jpg, jpeg, webp allowed")

    # File size check
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return ResponseHandler.validation_error("File must be under 2MB")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Unique filename — user_id + original extension, purane avatar ko overwrite karega
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f"user_{current_user_id}.{ext}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    avatar_url = f"/static/avatars/{filename}"
    UserModel.update_avatar_url(current_user_id, avatar_url)

    return ResponseHandler.success(
        data={"avatar_url": avatar_url},
        message="Avatar uploaded successfully"
    )