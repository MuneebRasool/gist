"""
User model for the application.
"""

from tortoise import fields, models
import bcrypt
from src.utils.encryption import encryption


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
    personality = fields.JSONField(null=True)
    nylas_email = fields.CharField(max_length=255, null=True)
    nylas_grant_id = fields.TextField(null=True, description="Encrypted Nylas grant ID")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    async def set_nylas_grant_id(self, grant_id: str) -> None:
        """Encrypt and store Nylas grant ID."""
        if not grant_id:
            return
        self.nylas_grant_id = encryption.encrypt(grant_id)

    def get_nylas_grant_id(self) -> str | None:
        """Decrypt and return Nylas grant ID."""
        if not self.nylas_grant_id:
            return None
        return encryption.decrypt(self.nylas_grant_id)

    def verify_password(self, password: str) -> bool:
        """Verify a password against its hash."""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    @staticmethod
    async def get_by_grant_id(grant_id: str):
        """Get a user by Nylas grant ID."""
        all_users = await User.filter(nylas_grant_id__not_isnull=True).all()
        for user in all_users:
            if user.get_nylas_grant_id() == grant_id:
                return user
        return None
    
    @staticmethod
    async def get_all_users_by_grant_id(grant_id:str):
        """Get all users by Nylas grant ID."""
        all_users = await User.filter(nylas_grant_id__not_isnull=True).all()
        users = []
        for user in all_users:
            if user.get_nylas_grant_id() == grant_id:
                users.append(user)
        return users
    
    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.name} ({self.email})"

    class PydanticMeta:
        exclude = ["password_hash"]
