# controllers/auth_controller.py
from flask import request, jsonify, g
from models.user_model import UserModel
from utils.encryption import encrypt_data, decrypt_data
from middleware.crypto_middleware import decrypt_request, encrypt_response
import jwt
import datetime
from functools import wraps
from config import JWT_SECRET, JWT_EXPIRY
from constants.messages import AuthMessages
from constants.status_codes import StatusCode
from utils.validators import AuthValidator
from utils.response_handler import ResponseHandler


# ── Token verify decorator ───────────────────────────────
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return ResponseHandler.unauthorized(AuthMessages.TOKEN_MISSING)

        try:
            decoded        = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            encrypted_data = decoded.get('data')
            if not encrypted_data:
                raise Exception('No payload found')
            current_user   = decrypt_data(encrypted_data)

        except jwt.ExpiredSignatureError:
            return ResponseHandler.unauthorized(AuthMessages.TOKEN_EXPIRED)
        except Exception as e:
            return ResponseHandler.unauthorized(AuthMessages.TOKEN_INVALID)

        return f(current_user, *args, **kwargs)
    return decorated


class AuthController:

    @staticmethod
    @decrypt_request       # ← request decrypt karo
    @encrypt_response      # ← response encrypt karo
    def register():
        # g.decrypted_body se data lo (request.get_json() nahi)
        data     = g.decrypted_body
        name     = data.get('name', '').strip()
        email    = data.get('email', '').strip()
        password = data.get('password', '').strip()

          # ── Validate ─────────────────────────────────
        errors = AuthValidator.validate_register(data)
        if errors:
            return ResponseHandler.validation_error(errors)

        existing = UserModel.find_by_email(email)
        if existing:
            return ResponseHandler.error(
                AuthMessages.EMAIL_ALREADY_EXISTS,
                StatusCode.CONFLICT
            )

        try:
            UserModel.create_user(
                name=name,
                email=email,
                password=password
            )
            return ResponseHandler.success(
                AuthMessages.REGISTER_SUCCESS,
                status_code=StatusCode.CREATED
            )
        except Exception as e:
            return ResponseHandler.server_error()

    @staticmethod
    @decrypt_request       # ← request decrypt karo
    @encrypt_response      # ← response encrypt karo
    def login():
        data     = g.decrypted_body
        email    = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # ── Validate ─────────────────────────────────
        errors = AuthValidator.validate_login(data)
        if errors:
            return ResponseHandler.validation_error(errors)

        # ── Business Logic ───────────────────────────
        user = UserModel.find_by_email(data['email'].strip())

        if not user or not UserModel.verify_password(
            data['password'].strip(), user['password']
        ):
            return ResponseHandler.unauthorized(
                AuthMessages.INVALID_CREDENTIALS
            )

        UserModel.update_login_status(user['id'], 1)

        # JWT payload encrypt karo
        user_payload   = {
            'user_id'  : user['id'],
            'name'     : user['name'],
            'email'    : user['email'],
            'user_role': user['user_role']
        }
        encrypted_data = encrypt_data(user_payload)
        jwt_payload    = {
            'data': encrypted_data,
            'exp' : datetime.datetime.utcnow() +
                    datetime.timedelta(hours=JWT_EXPIRY)
        }
        token = jwt.encode(jwt_payload, JWT_SECRET, algorithm='HS256')

        return ResponseHandler.success(
            AuthMessages.LOGIN_SUCCESS,
            data={
                'token': token,
                'user' : {
                    'id'               : user['id'],
                    'name'             : user['name'],
                    'email'            : user['email'],
                    'user_role'        : user['user_role'],
                    'user_login_status': True
                }
            }
        )


    @staticmethod
    @token_required
    @encrypt_response      # ← response encrypt karo
    def logout(current_user):
        try:
            UserModel.update_login_status(current_user['user_id'], 0)
            return ResponseHandler.success(AuthMessages.LOGOUT_SUCCESS)
        except Exception:
            return ResponseHandler.server_error()


    @staticmethod
    @token_required
    @encrypt_response
    def get_profile(current_user):
        user = UserModel.find_by_email(current_user['email'])

        if not user:
            return ResponseHandler.not_found('User not found')

        return ResponseHandler.success(
            AuthMessages.PROFILE_FETCHED_SUCCESSFULLY,
            data={
                'id'       : user['id'],
                'name'     : user['name'],
                'email'    : user['email'],
                'user_role': user['user_role']
            }
        )