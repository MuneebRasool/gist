from tortoise import fields, models
import bcrypt
from src.utils.encryption import encryption
from io import BytesIO
import joblib
from sklearn.linear_model import SGDRegressor
import numpy as np
import uuid
from typing import Optional, List


class User(models.Model):
    """
    User model that represents the users table in the database.
    """

    id = fields.UUIDField(pk=True)
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
    onboarding = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # One-to-One Relation with UserModel
    user_model: fields.OneToOneRelation["UserModel"]

    async def set_nylas_grant_id(self, grant_id: str) -> None:
        """Encrypt and store Nylas grant ID."""
        if grant_id:
            self.nylas_grant_id = encryption.encrypt(grant_id)

    def get_nylas_grant_id(self) -> str | None:
        """Decrypt and return Nylas grant ID."""
        return encryption.decrypt(self.nylas_grant_id) if self.nylas_grant_id else None

    def verify_password(self, password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8")) if self.password_hash else False

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    async def get_by_grant_id(grant_id: str):
        """Get user by Nylas grant ID."""
        users = await User.filter(nylas_grant_id__not_isnull=True).all()
        return next((user for user in users if user.get_nylas_grant_id() == grant_id), None)

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.name} ({self.email})"

    class PydanticMeta:
        exclude = ["password_hash"]



class UserModel(models.Model):
    """
    UserModel model that represents the user_models table in the database.
    Stores serialized SGDRegressor models for utility and cost predictions.
    """
    user = fields.OneToOneField("models.User", related_name="user_model", on_delete=fields.CASCADE)
    utility_model = fields.BinaryField(null=True, description="Serialized utility SGDRegressor model")
    cost_model = fields.BinaryField(null=True, description="Serialized cost SGDRegressor model")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_models"

    def __str__(self):
        # Use self.user.id directly instead of user_id property
        return f"Models for User {self.user.id}"

    # Serialization/Deserialization Helpers
    @staticmethod
    def _serialize_model(model) -> bytes:
        """Serialize an SGDRegressor model to bytes."""
        buffer = BytesIO()
        joblib.dump(model, buffer)
        # print("buffer.getvalue()")
        # print(buffer.getvalue())
        return buffer.getvalue()

    @staticmethod
    def _deserialize_model(model_bytes: bytes) -> SGDRegressor:
        """Deserialize bytes back into an SGDRegressor model."""
        if not model_bytes:
            return SGDRegressor()
        buffer = BytesIO(model_bytes)
        # print("buffer.getvalue()  deserialization")
        # print(buffer.getvalue())
        return joblib.load(buffer)

    # Instance Methods
    async def get_utility_model(self) -> SGDRegressor:
        """Retrieve and deserialize the utility model."""
        return self._deserialize_model(self.utility_model)

    async def get_cost_model(self) -> SGDRegressor:
        """Retrieve and deserialize the cost model."""
        return self._deserialize_model(self.cost_model)

    async def set_models(self, utility_model: SGDRegressor, cost_model: SGDRegressor) -> None:
        """Serialize and set the utility and cost models."""
        if not hasattr(utility_model, 'coef_'):
            utility_model.fit(np.array([[0]]), np.array([0]))
        if not hasattr(cost_model, 'coef_'):
            cost_model.fit(np.array([[0]]), np.array([0]))

        self.utility_model = self._serialize_model(utility_model)
        self.cost_model = self._serialize_model(cost_model)
        await self.save()

    @classmethod
    async def get_or_create(cls, user_id: str) -> "UserModel":
        """Get or create a UserModel instance."""
        user = await User.get(id=user_id)
        existing_model = await cls.filter(user=user).first()
        if existing_model:
            return existing_model
        new_model = await cls.create(user=user)
        return new_model
    


class Features(models.Model):
    """
    Features model that represents the features table in the database.
    Stores extracted utility and cost features for each task. 
    """
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="features", on_delete=fields.CASCADE)
    task_id = fields.CharField(max_length=255)
    features = fields.JSONField()
    cost = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "features"

    def __str__(self):
        return f"Features for Task {self.task_id} ({self.user.email})"
        
    @classmethod
    async def create_features(cls, user_id: str, task_id: str, utility_features: dict, cost_features: dict) -> "Features":
        """
        Create a new features record for a task
        
        Args:
            user_id: The ID of the user
            task_id: The ID of the task
            utility_features: Dictionary of utility features
            cost_features: Dictionary of cost features
            
        Returns:
            Features: The created features record
        """
        user = await User.get(id=user_id)
        
        features = await cls.create(
            id=uuid.uuid4(),
            user=user,
            task_id=task_id,
            features=utility_features,
            cost=cost_features
        )
        
        return features
    
    @classmethod
    async def get_by_task_id(cls, task_id: str) -> Optional["Features"]:
        """
        Get features by task ID
        
        Args:
            task_id: The ID of the task
            
        Returns:
            Optional[Features]: The features record if found, None otherwise
        """
        return await cls.filter(task_id=task_id).first()
    
    @classmethod
    async def get_by_user_id(cls, user_id: str) -> List["Features"]:
        """
        Get all features for a user
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List[Features]: List of features records for the user
        """
        user = await User.get(id=user_id)
        return await cls.filter(user=user).all()