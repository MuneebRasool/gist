"""
User model for the application.
"""

from tortoise import fields, models
import bcrypt


class User(models.Model):
    """
    User model that represents the users table in the database.
    """

    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    avatar = fields.CharField(max_length=255, null=True)
    password_hash = fields.CharField(max_length=128, null=True)
    is_active = fields.BooleanField(default=True)
    verified = fields.BooleanField(default=False)
    verification_code = fields.CharField(max_length=6, null=True)
    verification_code_expires_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def verify_password(self, password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.name} ({self.email})"

    class PydanticMeta:
        exclude = ["password_hash"]
