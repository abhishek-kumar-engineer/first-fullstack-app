# models/reset_token_model.py
import secrets
import datetime
from db import get_db_connection
from config import RESET_TOKEN_EXPIRY_MINUTES


class ResetTokenModel:

    @staticmethod
    def create_token(user_id: int) -> str:
        """
        random token is generated and stored in the database with an expiry time.
        """
        # Pehle purane tokens delete karo is user ke
        ResetTokenModel.delete_user_tokens(user_id)

        # Random secure token generate karo
        token = secrets.token_urlsafe(32)

        expires_at = (
            datetime.datetime.utcnow() +
            datetime.timedelta(minutes=RESET_TOKEN_EXPIRY_MINUTES)
        )

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO password_reset_tokens
                       (user_id, token, expires_at)
                       VALUES (%s, %s, %s)""",
                    (user_id, token, expires_at)
                )
                conn.commit()
            return token
        finally:
            conn.close()


    @staticmethod
    def find_valid_token(token: str):
        """
        Token valid hai? expired toh nahi? already used toh nahi?
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM password_reset_tokens
                       WHERE token      = %s
                       AND   expires_at > UTC_TIMESTAMP()
                       AND   is_used    = FALSE""",
                    (token,)
                )
                return cursor.fetchone()
        finally:
            conn.close()


    @staticmethod
    def mark_token_used(token: str):
        """
        Token use ho gaya — dobara use na ho sake
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE password_reset_tokens
                       SET is_used = TRUE
                       WHERE token = %s""",
                    (token,)
                )
                conn.commit()
        finally:
            conn.close()


    @staticmethod
    def delete_user_tokens(user_id: int):
        """
        Delete the all old tokens for this user (agar user ne multiple reset requests bheje hain)
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM password_reset_tokens
                       WHERE user_id = %s""",
                    (user_id,)
                )
                conn.commit()
        finally:
            conn.close()
    
    @staticmethod
    def update_password(user_id: int, hashed_password: str):
        """
        Update the user's password in the database.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """UPDATE users
                       SET password = %s
                       WHERE id = %s""",
                    (hashed_password, user_id)
                )
                conn.commit()
        finally:
            conn.close()