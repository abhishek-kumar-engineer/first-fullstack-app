# utils/validators.py
import re
from constants.messages import AuthMessages


class AuthValidator:

    @staticmethod
    def validate_register(data: dict) -> list:
        """
        Register form validate karo
        Return → list of error messages (empty list = valid ✅)
        """
        errors = []

        name     = data.get('name', '').strip()
        email    = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # ── Name validation ──────────────────────────
        if not name:
            errors.append(AuthMessages.NAME_REQUIRED)
        elif len(name) < 2:
            errors.append('Name must be at least 2 characters')
        elif len(name) > 100:
            errors.append('Name must not exceed 100 characters')

        # ── Email validation ─────────────────────────
        if not email:
            errors.append(AuthMessages.EMAIL_REQUIRED)
        elif not AuthValidator._is_valid_email(email):
            errors.append(AuthMessages.EMAIL_INVALID)

        # ── Password validation ──────────────────────
        if not password:
            errors.append(AuthMessages.PASSWORD_REQUIRED)
        else:
            if len(password) < 6:
                errors.append(AuthMessages.PASSWORD_TOO_SHORT)
            if not re.search(r'[A-Z]', password):
                errors.append(AuthMessages.PASSWORD_NO_UPPERCASE)
            if not re.search(r'\d', password):
                errors.append(AuthMessages.PASSWORD_NO_NUMBER)

        return errors   # [] = valid, [...] = errors


    @staticmethod
    def validate_login(data: dict) -> list:
        """
        Login form validate karo
        """
        errors = []

        email    = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email:
            errors.append(AuthMessages.EMAIL_REQUIRED)
        elif not AuthValidator._is_valid_email(email):
            errors.append(AuthMessages.EMAIL_INVALID)

        if not password:
            errors.append(AuthMessages.PASSWORD_REQUIRED)

        return errors


    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Email format check karo using regex
        valid   → abhi@test.com ✅
        invalid → abhi@test, abhi.com, @test.com ❌
        """
        pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))