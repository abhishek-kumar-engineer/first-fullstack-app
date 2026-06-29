# utils/email_helper.py
from flask_mail import Mail, Message
from config import (
    MAIL_USERNAME, MAIL_FROM_NAME, FRONTEND_URL
)

mail = Mail()   # app.py mein initialize hoga


def send_reset_email(to_email: str, user_name: str, reset_token: str):
    """
    Reset password email bhejo
    """
    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"

    subject = "Reset Your Password — First Fullstack App"

    # ── HTML Email body ───────────────────────────────
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px;
                 margin: 0 auto; padding: 20px;">

        <div style="background: #667eea; padding: 20px;
                    border-radius: 10px 10px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0;">🔐 Password Reset</h1>
        </div>

        <div style="background: #f9f9f9; padding: 30px;
                    border-radius: 0 0 10px 10px;">

            <p>Hi <strong>{user_name}</strong>,</p>

            <p>We received a request to reset your password.
               Click the button below to create a new password:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}"
                   style="background: #667eea; color: white;
                          padding: 14px 30px; text-decoration: none;
                          border-radius: 8px; font-weight: bold;
                          font-size: 16px;">
                    Reset My Password
                </a>
            </div>

            <p style="color: #666; font-size: 14px;">
                ⏰ This link will expire in
                <strong>15 minutes</strong>.
            </p>

            <p style="color: #666; font-size: 14px;">
                If you did not request this, please ignore this email.
                Your password will remain unchanged.
            </p>

            <hr style="border: none; border-top: 1px solid #ddd;">
            <p style="color: #999; font-size: 12px; text-align: center;">
                Auth App — Security Team
            </p>
        </div>
    </body>
    </html>
    """

    msg = Message(
        subject   = subject,
        sender    = (MAIL_FROM_NAME, MAIL_USERNAME),
        recipients= [to_email],
        html      = html_body
    )

    mail.send(msg)