# controllers/profile_controller.py

from flask import request
from models.user_model import UserModel
from controllers.auth_controller import token_required
from utils.response_handler import ResponseHandler
from constants.messages import AuthMessages
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@token_required
def get_my_profile(current_user):   # naam badla — clarity ke liye
    user_id = current_user.get('user_id')  # ya jo bhi actual key hai dict mein

    profile = UserModel.get_profile_by_id(user_id)

    if not profile:
        return ResponseHandler.not_found("User not found")

    return ResponseHandler.success(
        message=AuthMessages.PROFILE_FETCHED_SUCCESSFULLY,
        data=profile
    )


@token_required
def update_my_profile(current_user):
    current_user_id = current_user.get('user_id')
    data = request.get_json()

    if not data:
        return ResponseHandler.validation_error(["No data provided"])

    name = data.get('name')
    bio = data.get('bio')
    phone = data.get('phone')

    errors = []
    if bio and len(bio) > 500:
        errors.append("Bio must be under 500 characters")
    if phone and len(phone) > 20:
        errors.append("Invalid phone number")

    if errors:
        return ResponseHandler.validation_error(errors)

    success = UserModel.update_profile(current_user_id, name=name, bio=bio, phone=phone)

    if not success:
        return ResponseHandler.validation_error(["Nothing to update"])

    updated_profile = UserModel.get_profile_by_id(current_user_id)
    return ResponseHandler.success(
        message=AuthMessages.PROFILE_UPDATED_SUCCESSFULLY,
        data=updated_profile
    )


@token_required
def upload_avatar(current_user):
    current_user_id = current_user.get('user_id')
    if 'avatar' not in request.files:
        return ResponseHandler.validation_error(["No file uploaded"])

    file = request.files['avatar']

    if file.filename == '':
        return ResponseHandler.validation_error(["No file selected"])

    if not allowed_file(file.filename):
        return ResponseHandler.validation_error(["Only png, jpg, jpeg, webp allowed"])

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return ResponseHandler.validation_error(["File must be under 2MB"])

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f"user_{current_user_id}.{ext}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    avatar_url = f"/static/avatars/{filename}"
    UserModel.update_avatar_url(current_user_id, avatar_url)

    return ResponseHandler.success(
        message=AuthMessages.AVATAR_UPLOADED_SUCCESSFULLY,
        data={"avatar_url": avatar_url}
    )