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

    @staticmethod
    def get_profile_by_id(user_id):
        """
        Fetch user profile fields by user_id.
        Password field yahan return NAHI karte — security best practice.
        """
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT id, name, email, avatar_url, bio, phone, 
                        user_role, created_at, updated_at
                    FROM users
                    WHERE id = %s
                """
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def update_profile(user_id, name=None, bio=None, phone=None):
        """
        Partial update — sirf jo fields diye gaye hain wahi update honge.
        Dynamic query build karte hain taaki NULL se kisi field ko overwrite na karein.
        """
        fields = []
        values = []

        if name is not None:
            fields.append("name = %s")
            values.append(name)
        if bio is not None:
            fields.append("bio = %s")
            values.append(bio)
        if phone is not None:
            fields.append("phone = %s")
            values.append(phone)

        if not fields:
            return False  # kuch update karne layak nahi mila

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, tuple(values))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

    @staticmethod
    def update_avatar_url(user_id, avatar_url):
        """
        Separate method for avatar — kyunki avatar upload ka flow
        (file handling) baaki profile fields se alag hoga.
        """
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = "UPDATE users SET avatar_url = %s WHERE id = %s"
                cursor.execute(query, (avatar_url, user_id))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()