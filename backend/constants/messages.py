# constants/messages.py

class AuthMessages:
    # ── Register ───────────────────────────────
    REGISTER_SUCCESS        = 'Registration successful!'
    EMAIL_REQUIRED          = 'Email is required'
    NAME_REQUIRED           = 'Name is required'
    PASSWORD_REQUIRED       = 'Password is required'
    EMAIL_INVALID           = 'Please enter a valid email address'
    PASSWORD_TOO_SHORT      = 'Password must be at least 6 characters'
    PASSWORD_NO_UPPERCASE   = 'Password must contain at least one uppercase letter'
    PASSWORD_NO_NUMBER      = 'Password must contain at least one number'
    EMAIL_ALREADY_EXISTS    = 'Email is already registered'

    # ── Login ──────────────────────────────────
    LOGIN_SUCCESS           = 'Login successful!'
    INVALID_CREDENTIALS     = 'Invalid email or password'

    # ── Logout ─────────────────────────────────
    LOGOUT_SUCCESS          = 'Logged out successfully!'

    # ── Token ──────────────────────────────────
    TOKEN_MISSING           = 'Access token is missing'
    TOKEN_EXPIRED           = 'Token has expired — please login again'
    TOKEN_INVALID           = 'Invalid token'

    # ── General ────────────────────────────────
    SERVER_ERROR            = 'Something went wrong — please try again'
    INVALID_REQUEST_FORMAT  = 'Invalid request format'
    DECRYPTION_FAILED       = 'Request could not be processed'

    # ── Reset Password messages ────────────────────────
    RESET_EMAIL_SENT        = 'Password reset link sent to your email'
    RESET_TOKEN_INVALID     = 'Reset link is invalid or has expired'
    RESET_TOKEN_USED        = 'Reset link has already been used'
    RESET_SUCCESS           = 'Password reset successful! Please login.'
    NEW_PASSWORD_REQUIRED   = 'New password is required'
    USER_NOT_FOUND          = 'No account found with this email'

    # ── Profile messages ────────────────────────
    PROFILE_FETCHED_SUCCESSFULLY = "Profile fetched successfully"
    PROFILE_UPDATED_SUCCESSFULLY = "Profile updated successfully"
    AVATAR_UPLOADED_SUCCESSFULLY = "Avatar uploaded successfully"