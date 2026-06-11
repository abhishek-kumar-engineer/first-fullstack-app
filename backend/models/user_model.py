# models/user_model.py
import bcrypt
from db import get_db_connection

class UserModel:

    @staticmethod
    def find_by_email(email):
        """Email se user dhundo"""
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE email = %s", (email,)
                )
                return cursor.fetchone()   # dict ya None
        finally:
            conn.close()

    @staticmethod
    def create_user(name, email, password):
        """Naya user insert karo"""
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, hashed)
                )
                conn.commit()
                return cursor.lastrowid     # naye user ka id return karo
        finally:
            conn.close()
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Password match karo — True/False return karta hai"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def update_login_status(user_id, status):
        """Login/Logout pe status update karo"""
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE users 
                       SET user_login_status = %s 
                       WHERE id = %s""",
                    (status, user_id)
                )
                conn.commit()
        finally:
            conn.close()