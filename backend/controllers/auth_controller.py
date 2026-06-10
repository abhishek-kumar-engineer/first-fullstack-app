# controllers/auth_controller.py
from flask import request, jsonify
from models.user_model import UserModel

class AuthController:

    @staticmethod
    def register():
        data     = request.get_json()
        name     = data.get('name', '').strip()
        email    = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Validation
        if not name or not email or not password:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400

        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }), 400

        # Email already exists?
        existing = UserModel.find_by_email(email)
        if existing:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409

        # User banao
        UserModel.create_user(name, email, password)
        return jsonify({
            'success': True,
            'message': 'Registration successful!'
        }), 201

    @staticmethod
    def login():
        import jwt
        import datetime
        from config import JWT_SECRET, JWT_EXPIRY

        data     = request.get_json()
        email    = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # 1. Validation
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400

        # 2. User dhundo database mein
        user = UserModel.find_by_email(email)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'  # intentionally same message
            }), 401

        # 3. Password verify karo
        password_match = UserModel.verify_password(password, user['password'])
        if not password_match:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401

        # 4. JWT Token generate karo
        payload = {
            'user_id' : user['id'],
            'name'    : user['name'],
            'email'   : user['email'],
            'exp'     : datetime.datetime.utcnow() +
                        datetime.timedelta(hours=JWT_EXPIRY)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        # 5. Token return karo
        return jsonify({
            'success' : True,
            'message' : 'Login successful!',
            'token'   : token,
            'user'    : {
                'id'   : user['id'],
                'name' : user['name'],
                'email': user['email']
            }
        }), 200