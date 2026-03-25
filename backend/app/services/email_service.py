import resend
from app.core.config import settings

resend.api_key = settings.RESEND_API_KEY


class EmailService:
    async def send_password_reset(self, email: str, reset_url: str) -> None:
        resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": email,
            "subject": "Reset Your Planify Password",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #4F46E5;">Reset Your Password</h2>
                <p>You requested a password reset for your Planify account.</p>
                <p>Click the button below to reset your password. This link will expire in <strong>1 hour</strong>.</p>
                <a href="{reset_url}"
                   style="display: inline-block; background-color: #4F46E5; color: white;
                          padding: 12px 24px; border-radius: 6px; text-decoration: none;
                          margin: 16px 0;">
                    Reset Password
                </a>
                <p style="color: #6B7280; font-size: 14px;">
                    If you didn't request this, you can safely ignore this email.
                </p>
                <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 24px 0;">
                <p style="color: #9CA3AF; font-size: 12px;">Planify — Task & Project Management</p>
            </div>
            """,
        })